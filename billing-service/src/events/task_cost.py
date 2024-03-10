from datetime import datetime

from src.models.task import TaskCost


def send_task_cost_added_event(task_cost: TaskCost, task_public_id: str) -> None:
    producer = get_producer(ProducerTypes.TASKCOSTS_BC)
    event = TaskCostAddedEventSchema(
        data={
            "public_id": task_cost.public_id,
            "task_public_id": task_public_id,
            "debit_cost": task_cost.debit_cost,
            "credit_cost": task_cost.credit_cost,
        },
        produced_at=datetime.utcnow(),
    )
    producer.publish_message(
        event.json().encode("utf-8"),
        get_routing_key(event.title, event.version),
    )
