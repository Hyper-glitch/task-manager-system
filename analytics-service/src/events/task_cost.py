import logging

from schema_registry.models.v1.task_cost_added_event import TaskCostAddedEventSchema

from src.config import settings

logger = logging.getLogger(settings.project)


class TaskCostEventService:
    def __init__(
        self,
        task_cost_repo: TaskCostRepository,
    ):
        self.task_cost_repo = task_cost_repo

    def _create_task_cost(self, event: TaskCostAddedEventSchema) -> None:
        data = event.data.dict()
        task = self.task_cost_repo.create(**data)
        logger.info(f"{task = } created")

    def process_task_cost_event_message(self, message: bytes) -> None:
        event = TaskCostAddedEventSchema.model_validate_json(message)
        logger.info(f"Processing event: {event}")
        self._create_task_cost(event)
