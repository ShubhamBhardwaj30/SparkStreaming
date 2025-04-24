# Spark Kafka Analytics System

This project sets up a simple analytics pipeline using Apache Spark, Kafka, and Docker Compose. It includes:

- Kafka (broker + zookeeper)
- Spark master and workers
- Python job for Spark streaming from Kafka
- Job submission container

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
```

These JARs are required for Spark to read from Kafka.

3. **Start the Docker Compose environment**

```bash
docker-compose up
```

This will:
- Launch Zookeeper and Kafka
- Start Spark master and workers
- Run a one-time Spark job via `spark-job-submitter` after a short delay

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
  --jars /opt/spark/jars/spark-sql-kafka-0-10_2.12-3.3.4.jar,/opt/spark/jars/kafka-clients-3.3.2.jar \
  /opt/spark-apps/spark_stream_analyzer.py
```

## 🧪 Verifying Kafka Topic

You can verify Kafka messages are flowing by inspecting the console output of the job or producing messages manually using Kafka CLI or a Python script.

## 🛠 Configuration

- Spark startup and job submission is handled via `setup.sh`
- Python Kafka dependencies are installed automatically inside the Spark containers
