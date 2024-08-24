from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from send_redis_data import store_in_redis
from pyspark.sql.functions import col, length
import logging
import time


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
            .option("subscribe", "vote_passthrough") \
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
        return df
    except ValueError as e:
        logger.error(f'Error: type not found - {str(e)}')
        raise e
    except Exception as e:
        logger.error(f'Error: Unexpected error - {str(e)}')
        raise e


# VERIFICATION DATA INTEGRITY
def df_verification_and_validation(df):
    df = df.withColumn("is_valid", 
                       (col('key').isNotNull()) & 
                       (col('key').cast('string').isNotNull()) &
                       (col('value').isNotNull()))

    return df


# PRINT THE VALUES IN CONSOLE
def write_values_from_kafka():
    spark = spark_session()
    kafka_stream = read_from_stream_kafka(spark)
    df = casting_data(kafka_stream)
    df = df_verification_and_validation(df)

    valid_df = df.filter(col("is_valid") == True)

    try:
        query = valid_df.writeStream \
            .foreachBatch(store_in_redis) \
            .outputMode("append") \
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
