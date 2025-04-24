from pyspark.sql import SparkSession
from pyspark.sql.functions import col

def main():
    # Initialize Spark session for Docker-based Spark cluster
    spark = SparkSession \
        .builder \
        .appName("KafkaSparkStreaming") \
        .master("spark://spark-master:7077") \
        .getOrCreate()

    # Define the Kafka source
    kafka_stream = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "broker:29092") \
        .option("subscribe", "analytics") \
        .option("startingOffsets", "latest") \
        .load()

    # Process the data
    data = kafka_stream \
        .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Define the output
    query = data \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .trigger(processingTime="10 seconds") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()