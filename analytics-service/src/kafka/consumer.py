import logging

from confluent_kafka import Consumer, KafkaError

from src.config import settings

logger = logging.getLogger(settings.project)


class EventsConsumer:
    def __init__(self, topic: str, callback) -> None:
        self.consumer = Consumer(
            {
                "bootstrap.servers": settings.bootstrap_servers,
                "group.id": settings.group_id,
                "auto.offset.reset": "earliest",
            }
        )
        self.consumer.subscribe([topic])
        self.consumer.subscribe(callback)

    def process_message(self) -> None:
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                print("Received message:", msg.value)
        except Exception as exc:
            logger.error(f"Error during processing: {exc}")
            raise
