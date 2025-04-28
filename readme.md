# Spark Kafka Analytics System

This project sets up a simple analytics pipeline using Apache Spark, Kafka, and Docker Compose. It includes:

- Kafka (broker + zookeeper)
- Spark master and workers
- Python job for Spark streaming from Kafka
- Postgres DB
- Pgadmin
- Jupyter lab

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



Submit the job manually to spak cluster:

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

## 🛠️ Synthetic Data Generation and Testing

You can use the provided helper scripts to simulate data production and consumption for testing.

### Produce Synthetic Data

Run the producer script to generate random events and send them to the `analytics` topic:

```bash
python helper/analytics_producer.py
```

This will create and send 300 random messages spaced out with random delays.

### Consume and Verify Messages

Run the consumer script to read and display messages from the `analytics` topic:

```bash
python helper/analytics_consumer.py
```

This will print each incoming message to the console, verifying that data is being produced and available on Kafka.


## 🛠 Configuration

- Spark startup and job submission is handled via `setup.sh`
- Python Kafka dependencies are installed automatically inside the Spark containers

## 📈 Viewing Processed Data

After submitting the Spark job, you can view the results:

- Raw streaming events are stored in the `stream_data` table.
- Aggregated results (windowed aggregation) are stored in the `aggregated_stream_data` table.


To connect to Postgres and query the tables:

```bash
docker exec -it postgres psql -U analytics_user -d analytics_db
```

Example queries:

```sql
SELECT * FROM stream_data LIMIT 10;
SELECT * FROM aggregated_stream_data LIMIT 10;
```

### Viewing Data Using pgAdmin

You can also use **pgAdmin** to connect to the database and view the tables visually.

Connection details for pgAdmin:

- Host: `postgres`
- Port: `5432`
- Username: `analytics_user`
- Password: `analytics_pass`
- Database: `analytics_db`

Once connected, navigate to the `stream_data` and `aggregated_stream_data` tables to view the raw and aggregated streaming data.

## 🔌 Ports for Localhost Connections

These are the default ports mapped by Docker Compose for local access:

- **Kafka Broker:**  
  - `localhost:9092` (for client connections)
  - `localhost:29092` (for internal Docker connections)
- **Zookeeper:**  
  - `localhost:22181`
- **Spark Master UI:**  
  - [http://localhost:9090](http://localhost:9090)
- **Spark Worker A UI:**  
  - [http://localhost:9091](http://localhost:9091)
- **Spark Worker B UI:**  
  - [http://localhost:9093](http://localhost:9093)
- **JupyterLab:**  
  - [http://localhost:8888](http://localhost:8888)
- **Postgres:**  
  - `localhost:5432`
- **pgAdmin:**  
  - [http://localhost:8081](http://localhost:8081)