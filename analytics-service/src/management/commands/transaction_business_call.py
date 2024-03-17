from src.events import trans_events_service
from src.kafka.consumer import EventsConsumer


def transaction_business_call_consumer():
    consumer = EventsConsumer(
        topic="transactions", callback=trans_events_service.process_trans_event_message
    )
    consumer.process_message()
