#!/bin/bash

echo "Installing Python dependencies..."
pip install kafka-python

if [ "$SPARK_WORKLOAD" = "worker" ]; then
  echo "Registering Spark worker with master at $SPARK_MASTER"
  /opt/bitnami/spark/bin/spark-class org.apache.spark.deploy.worker.Worker "$SPARK_MASTER"
elif [ "$SPARK_WORKLOAD" = "master" ]; then
  echo "Starting Spark master..."
  /opt/bitnami/scripts/spark/run.sh
else
  echo "Spark workload is set to '$SPARK_WORKLOAD'. No action defined."
fi
