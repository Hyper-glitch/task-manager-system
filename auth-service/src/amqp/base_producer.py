import logging
from json import dumps
from typing import Any

from kafka import KafkaProducer

from src.config import settings

logger = logging.getLogger(settings.project)


class BaseProducer:
    def __init__(self, config):
        self._config = config
        self._connection = None
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda v: dumps(v).encode("utf-8"),
        )

    @property
    def is_closed_connection(self) -> bool:
        return not self._connection or self._connection.is_closed

    @property
    def is_closed_channel(self) -> bool:
        return not self._channel or self._channel.is_closed

    def _open_connection(self) -> None:
        if self.is_closed_connection:
            parameters = get_connection_params(self._config)
            logger.info(
                f"Connecting to host={parameters.host} "
                f"port={parameters.port} "
                f"virtual_host={parameters.virtual_host}>"
            )
            self._connection = pika.BlockingConnection(parameters)

        if self.is_closed_channel:
            self._channel = self._connection.channel()

        if self._init_exchange is True:
            logger.info(
                f"Creating a new exchange. "
                f"Exchange: {self._config.exchange.name}"
            )
            self._channel.exchange_declare(  # type: ignore
                exchange=self._config.exchange.name,
                exchange_type=self._config.exchange.type.value,
                durable=self._config.exchange.durable,
            )
            self._init_exchange = False

    def send(self, value: dict[str, Any]) -> None:
        if self.is_closed_connection or self.is_closed_channel:
            self._open_connection()

        if not self._channel:
            raise Exception("Channel is not initialized")

        try:
            self.producer.send(
                topic=self._config.exchange.name,
                value=value,
            )
        except Exception as exc:
            logger.error(
                f"Cannot send payload to `{self._config.exchange.name}` kafka topic. Reason: {exc}"
            )
        else:
            logger.info(
                f"Publishing to topic {self._config.exchange.name}, message {value}"
            )
            self.producer.flush()
