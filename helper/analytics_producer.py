from kafka import KafkaProducer, KafkaConsumer
import time
import json
import random
# Connect to Kafka
producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(300):
    current_time = time.time()
    local_time = time.localtime(current_time)

    data = {
        "user_id": random.randint(1000, 9999),
        "event_type": random.choice(["click", "view", "purchase"]),
        "value": round(random.uniform(10.0, 500.0), 2),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    }

    producer.send('analytics', json.dumps(data).encode('utf-8'))
    print(f"Sent message {i+1}: {data}")
    time.sleep(random.uniform(5.0, 10.0))  # Introduce varied delay to space out data

# Flush the producer to ensure all messages are sent
producer.flush()

# Close the producer
producer.close()
