FROM bitnami/spark:3.2.0

WORKDIR /app

USER root

RUN mkdir -p /tmp/spark /tmp/spark/logs && \
    chown -R 1001:1001 /tmp/spark /tmp/spark/logs


RUN pip install pyspark kafka-python

COPY log4j.properties /opt/bitnami/spark/conf/

USER 1001

CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0", "--conf", "spark.executor.logs.rolling.maxRetainedFiles=0", "--conf", "spark.driver.logs.rolling.maxRetainedFiles=0", "--conf", "spark.driver.extraJavaOptions=-Divy.cache.dir=/tmp -Divy.home=/tmp", "spark_process.py"]