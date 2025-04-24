from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

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

    # Define schema for the synthetic JSON structure
    schema = StructType([
        StructField("user_id", IntegerType(), True),
        StructField("event_type", StringType(), True),
        StructField("value", DoubleType(), True),
        StructField("timestamp", StringType(), True)
    ])

    # Process the data
    data = kafka_stream \
        .selectExpr("CAST(value AS STRING) as json_str") \
        .select(from_json(col("json_str"), schema).alias("data")) \
        .select("data.*")

    # Write the processed data to PostgreSQL
    data.writeStream \
        .foreachBatch(lambda batch_df, _: batch_df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://postgres:5432/analytics_db") \
            .option("dbtable", "stream_data") \
            .option("user", "analytics_user") \
            .option("password", "analytics_pass") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()) \
        .outputMode("append") \
        .start() \
        .awaitTermination()

if __name__ == "__main__":
    main()