import logging

from confluent_kafka import Producer

from src.config import settings

logger = logging.getLogger(settings.project)


class EventsProducer:
    def __init__(self) -> None:
        self.producer = Producer(
            {
                "bootstrap.servers": settings.bootstrap_servers,
                "group.id": settings.group_id,
            }
        )

    def send(self, value: str | bytes, topic: str) -> None:
        try:
            self.producer.produce(topic=topic, value=value)
        except Exception as exc:
            logger.error(f"Cannot send payload to `{topic}` kafka topic. Reason: {exc}")
        else:
            logger.info(f"Publishing to topic {topic}, message {value}")
            self.producer.flush()
