from datetime import datetime
from typing import Any

from src.config import settings
from src.dto.api.task import TaskDTO
from src.dto.events.task import TaskCreatedEventDTO, TaskEventDTO, TaskAssignedEventSchema, TaskNewAssigneeDTO
from src.kafka.manager import KafkaManager
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository
from src.services.exceptions import TaskNotFound


class TaskService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository, kafka: KafkaManager):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.kafka = kafka

    def get_task(self, task_id: int) -> TaskDTO:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFound

        task_dto = TaskDTO.from_orm(task)
        return task_dto

    def add_task(self, data: dict[str, Any]) -> TaskDTO:
        dto = TaskDTO.model_validate(data)
        task = self.task_repo.create_task(dto)
        old_assignee_public_id = task.assignee.public_id

        user, *_ = self.user_repo.get_random_employees(lock=True)
        self.task_repo.assign_to_user(user_id=user.id, task=task)
        data_event = TaskCreatedEventDTO(
            data=TaskEventDTO.from_orm(task),
            produced_at=datetime.utcnow(),
            version=2,
        )
        self.kafka.send(value=data_event.model_dump(mode="json"), topic=settings.data_streaming_topic)

        business_event = TaskAssignedEventSchema(
            data=TaskNewAssigneeDTO(
                public_id=task.public_id,
                old_assignee_public_id=old_assignee_public_id,
                new_assignee_public_id=user.public_id,
            ),
            produced_at=datetime.utcnow(),
        )
        self.kafka.send(value=business_event.model_dump(mode="json"), topic=settings.business_event_topic)
        return TaskDTO.from_orm(task)
