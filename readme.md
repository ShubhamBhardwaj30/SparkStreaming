# Spark Kafka Analytics System

This project sets up a simple analytics pipeline using Apache Spark, Kafka, and Docker Compose. It includes:

- Kafka (broker + zookeeper)
- Spark master and workers
- Python job for Spark streaming from Kafka
- Postgres DB

## 🚀 How to Start

1. **Clone the repo and navigate to the project directory**

```bash
git clone <repo-url>
cd analytics
```

2. **Prepare Kafka JARs**

Create a `jars` directory in the root of the project if it doesn't exist:

```bash
mkdir -p jars
```

Download the required Kafka JARs from Maven Central:

```bash
curl -L -o jars/spark-sql-kafka-0-10_2.12-3.3.4.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.3.4/spark-sql-kafka-0-10_2.12-3.3.4.jar

curl -L -o jars/kafka-clients-3.3.2.jar https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.2/kafka-clients-3.3.2.jar

curl -L -o jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.3.0/spark-token-provider-kafka-0-10_2.12-3.3.0.jar

curl -L -o jars/commons-pool2-2.11.1.jar https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

curl -L -o jars/postgresql-42.7.3.jar https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar
```

These JARs are required for Spark to read from Kafka.

3. **Start the Docker Compose environment**

```bash
docker-compose down && docker-compose up --build -d
```

This will:
- Launch Zookeeper and Kafka
- Start Spark master and workers
- Start the postgres DB and create the table


4. **Create tables if they were not greated by the Init script using the folllowing on PGADMIN**

```SQL
CREATE TABLE IF NOT EXISTS stream_data (
    user_id INTEGER,
    event_type TEXT,
    value DOUBLE PRECISION,
    timestamp TEXT
);

CREATE TABLE IF NOT EXISTS public.aggregated_stream_data
(
    window_start timestamp without time zone,
    window_end timestamp without time zone,
    event_type text COLLATE pg_catalog."default",
    total_value double precision,
    average_value double precision,
    event_count integer
)
```

## 📦 Job Submission

The job is defined in the file:

```text
apps/spark_stream_analyzer.py
```

The `spark-job-submitter` container waits 30 seconds and then runs this job using `spark-submit`, with the necessary JARs mounted and classpath configured.

If you want to submit additional jobs manually:

```bash
docker exec -it spark-master spark-submit \
  --master spark://spark-master:7077 \
  --jars /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.3.0.jar,\
/opt/spark/jars/kafka-clients-2.8.0.jar,\
/opt/spark/jars/postgresql-42.7.3.jar,\
/opt/spark/jars/spark-token-provider-kafka-0-10_2.12-3.3.0.jar,\
/opt/spark/jars/commons-pool2-2.11.1.jar \
  --conf "spark.driver.extraClassPath=/opt/spark/jars/*" \
  --conf "spark.executor.extraClassPath=/opt/spark/jars/*" \
  /opt/spark-apps/spark_stream_analyzer.py
```

## 🧪 Verifying Kafka Topic

You can verify Kafka messages are flowing by inspecting the console output of the job or producing messages manually using Kafka CLI or a Python script.

## 🛠 Configuration

- Spark startup and job submission is handled via `setup.sh`
- Python Kafka dependencies are installed automatically inside the Spark containers

## 🧪 Connect to PG
bash
```
docker exec -it postgres psql -U analytics_user -d analytics_db
```
Run your select query to see the data
