from src.kafka.consumer import EventsConsumer
from src.services import user_event_service


def user_data_streaming_events_consumer() -> None:
    consumer = EventsConsumer(
        topic="users-stream",
        callback=user_event_service.process_user_event_message,
    )
    consumer.process_message()
