from src.kafka.base_producer import BaseProducer
from src.conf.amqp import AMQPConfigSettings
from src.config import settings
from src.enums.events import EventTypes


class UserEventsProducer(BaseProducer):
    def open_connection(self) -> None:
        self._open_connection()


_producers: dict[EventTypes, UserEventsProducer | None] = {
    EventTypes.BUSINESS_CALL: None,
    EventTypes.DATA_STREAMING: None,
}


_config_map: dict[EventTypes, AMQPConfigSettings] = {
    EventTypes.BUSINESS_CALL: settings.amqp.users_bc_amqp,
    EventTypes.DATA_STREAMING: settings.amqp.users_ds_amqp,
}


def create_producer(event_type: EventTypes) -> UserEventsProducer:
    config: AMQPConfigSettings = _config_map[event_type]
    producer = UserEventsProducer(config)
    global _producers
    _producers[event_type] = producer
    return producer


def get_producer(event_type: EventTypes) -> UserEventsProducer:
    producer = _producers[event_type]
    if not producer:
        return create_producer(event_type)
    return producer
