from confluent_kafka import Producer

# Create asynchronous Kafka producer
producer = Producer({"bootstrap.servers": "localhost:9092"})

# Publish messages to topics asynchronously
producer.produce("topic1", b"Hello from topic1", callback=delivery_callback)
producer.produce("topic2", b"Hello from topic2", callback=delivery_callback)


# Flush the producer's message queue
producer.flush()
