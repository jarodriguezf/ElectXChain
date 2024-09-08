import sys
import os
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
from db_connection.db import ShowsDataDbUsers
from decrypt_validate.load_priv_key_system import load_private_system_key
from decrypt_validate.process_signature import validate_encryption
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from pyspark.sql.functions import col, udf
from pyspark.sql.types import BooleanType, StringType, StructType, StructField
import logging

logging.basicConfig(level=logging.ERROR,
                     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('py4j')
logger.setLevel(logging.ERROR)

spark_logger = logging.getLogger('org.apache.spark')
spark_logger.setLevel(logging.ERROR)


# SPARK SESSION
def spark_session():
    try:
        spark = SparkSession.builder \
            .appName("SparkKafkaStreaming") \
            .getOrCreate()
        logger.info('Spark context created successfully')
        return spark
    except Exception as e:
        logger.error(f'Error: Spark context can\'t be built - {str(e)}')
        raise e


# READ FROM KAFKA IN STREAM
def read_from_stream_kafka(spark):
    try:
        kafka_stream = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "kafka_host:9093") \
            .option("subscribe", "vote_result") \
            .option("startingOffsets", "latest") \
            .load()
        logger.info('Data successfully read from kafka stream')
        return kafka_stream
    except AnalysisException as e:
        logger.error(f'Error: In the processing of data from kafka - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'Error: Unexpected error - {str(e)}')
        raise e
    

# CASTING THE DATA IN DF
def casting_data(kafka_stream):
    try:
        df = kafka_stream.selectExpr("CAST(key AS STRING)", "value")
        logger.info('Casting realized correctly')
        #return df.withColumn("value", col("value").cast("binary"))
        return df
    except ValueError as e:
        logger.error(f'Error: type not found - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'Error: Unexpected error - {str(e)}')
        raise e


# VERIFICATION DATA INTEGRITY
def df_verification_and_validation(df):
    df =  df.withColumn("is_valid", 
                       (col('key').isNotNull()) & 
                       (col('key').cast('string').isNotNull()) &
                       (col('value').isNotNull()))
    return df


# DECRYPT AND VALIDATE THE SIGNATURE
def validate_signature(df, epoch_id):
    getUserData = ShowsDataDbUsers()
    
    # PROCESS THE KEY
    distinct_ids = df.select("key").distinct().collect()
    
    for row in distinct_ids:
        id = row["key"]
        pub_key_user = getUserData.show_pub_key_user(id)
        vote_user = getUserData.show_votehashed_user(id)
        
        if pub_key_user is None or vote_user is None:
            logger.error(f'Error: Missing data for id: {id}')
            continue
        
        # VALIDATE THE SIGNATURE WITH THE USER VOTE
        def validate_row(signature_AES_RSA):
            if isinstance(signature_AES_RSA, bytearray):
                signature_AES_RSA = bytes(signature_AES_RSA)

            system_private_key_pem = load_private_system_key('system_private_key.pem')

            return validate_encryption(
                encrypted_data=signature_AES_RSA,
                system_private_key_pem=system_private_key_pem,
                user_public_key_der=pub_key_user,
                original_message=vote_user
            )
        validate_udf = udf(validate_row, BooleanType())
        df = df.withColumn("is_valid", validate_udf(col("value")))
    df.show(truncate=False)


# PRINT THE VALUES IN CONSOLE
def write_values_from_kafka():
    spark = spark_session()
    kafka_stream = read_from_stream_kafka(spark)
    df = casting_data(kafka_stream)
    df = df_verification_and_validation(df)
    valid_df = df.filter(col("is_valid") == True) # VALIDATE OF THE ROW IS TRUE

    try:
        query = valid_df.writeStream \
            .outputMode("append") \
            .foreachBatch(validate_signature) \
            .start()

        logger.info('Streaming query started')
        logger.info('Awaiting termination...')

        query.awaitTermination()
    except Exception as e:
        logger.error(f'Error: Streaming query failed - {str(e)}')
        raise e
    finally:
        logger.info('Spark session closed')
        spark.stop()

if __name__ == '__main__':
    write_values_from_kafka()