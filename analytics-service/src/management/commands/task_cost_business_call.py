from src.events import task_cost_events_service
from src.kafka.consumer import EventsConsumer


def task_cost_business_call_consumer():
    consumer = EventsConsumer(
        topic="task-cost",
        callback=task_cost_events_service.process_task_cost_event_message,
    )
    consumer.process_message()
