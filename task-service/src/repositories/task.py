from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.dto.api.task import TaskDTO
from src.enums.status import TaskStatus
from src.models.task import Task
from src.models.user import User


class TaskRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_id(
            self, task_id: int, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(Task).outerjoin(User)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(Task.id == task_id).first()

    def create_task(self, dto: TaskDTO) -> Task:
        task = Task(**dto.model_dump())
        self._session.add(task)
        return task

    def assign_to_user(self, user_id: int, task: Task) -> None:
        task.assignee_id = user_id
        self._session.commit()

    def status_done(self, task: Task) -> None:
        task.status = TaskStatus.DONE
        self._session.commit()
