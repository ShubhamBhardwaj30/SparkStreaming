from kafka import KafkaProducer, KafkaConsumer

# Connect to Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(1):
    # Send a message to the 'analytics' topic
    producer.send('analytics', "Hello Kafka, This is working".format(i).encode('utf-8'))

# Flush the producer to ensure all messages are sent
producer.flush()

# Close the producer
producer.close()
