from src.config import settings
from src.kafka.consumer import consume_message


def user_business_call_events_consumer() -> None:
    consume_message(topic_name=settings.business_event_topic)


def user_data_streaming_events_consumer() -> None:
    consume_message(topic_name=settings.data_streaming_topic)
