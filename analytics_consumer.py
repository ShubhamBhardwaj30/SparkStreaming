from kafka import KafkaProducer, KafkaConsumer


# To consume messages from the 'analytics' topic
consumer = KafkaConsumer(
    'analytics',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest'
)

# Print messages from the consumer
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")