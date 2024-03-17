from src.events import user_events_service
from src.kafka.consumer import EventsConsumer


def user_business_call_consumer():
    consumer = EventsConsumer(
        topic="users", callback=user_events_service.process_user_event_message
    )
    consumer.process_message()
