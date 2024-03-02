import logging
import time
from json import dumps, loads
from typing import Any

from kafka3 import KafkaProducer, KafkaConsumer

from src.config import settings

logger = logging.getLogger(settings.project)


class KafkaManager:
    def __init__(self):
        self.connections = {}
        self.producer = KafkaProducer(
            bootstrap_servers=settings.bootstrap_servers,
            value_serializer=lambda v: dumps(v).encode("utf-8"),
        )

    def connect(self, topic) -> None:
        attempt = 1
        while True:
            logger.info(f"Connecting to Kafka topic `{topic}`... (Attempt: {attempt})")
            try:
                self.connections[topic] = KafkaConsumer(
                    topics=topic,
                    group_id=settings.task_group_id,
                    bootstrap_servers=settings.bootstrap_servers,
                    enable_auto_commit=False,
                    max_poll_interval_ms=settings.max_pool_interval_ms,
                    value_deserializer=lambda x: loads(x.decode("utf-8"))
                    if x is not None
                    else None,
                )
            except Exception as exc:
                logger.error(f"Cannot connect to kafka for host {settings.kafka_host}. Reason: {exc}")
                time.sleep(settings.reconnect_waiting)
                attempt += 1
            else:
                logger.info("Connect to Kafka is successful.")
                break

    def send(self, value: dict[str, Any], topic: str) -> None:
        try:
            self.producer.send(topic=topic, value=value)
        except Exception as exc:
            logger.error(
                f"Cannot send payload to `{topic}` kafka topic. Reason: {exc}"
            )
        else:
            logger.info(
                f"Publishing to topic {topic}, message {value}"
            )
            self.producer.flush()
