from kafka import KafkaProducer, KafkaConsumer
import time
# Connect to Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(1):
    # Send a message to the 'analytics' topic
    current_time = time.time()
    local_time = time.localtime(current_time)

    hour = local_time.tm_hour
    minute = local_time.tm_min
    second = local_time.tm_sec
    producer.send('analytics', "Hello Kafka, This is working, The time is {}:{}:{} ".format(hour, minute, second).encode('utf-8'))

# Flush the producer to ensure all messages are sent
producer.flush()

# Close the producer
producer.close()
