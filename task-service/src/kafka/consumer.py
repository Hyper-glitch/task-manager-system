from kafka3 import KafkaConsumer

from src.config import settings
from src.services import user_event_service


def consume_message(topic_name):
    consumer = KafkaConsumer(
        bootstrap_servers=settings.bootstrap_servers, auto_offset_reset='earliest'
    )
    consumer.subscribe([topic_name])
    while True:
        try:
            records = consumer.poll(timeout_ms=1000)
            for topic_data, consumer_records in records.items():
                for consumer_record in consumer_records:
                    user_event_service.process_user_event_message(message=consumer_record)
            continue
        except Exception as e:
            print(e)
            continue
