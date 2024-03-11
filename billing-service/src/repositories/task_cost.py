from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.dto.task import TaskDTO
from src.models.task import TaskCost


class TaskCostRepository:
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def get_by_task_id(
        self, task_id: int, lock: bool = False, **lock_params: Any
    ) -> TaskCost | None:
        query = self._session.query(TaskCost)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(TaskCost.task_id == task_id).first()

    def add(self, task_dto: TaskDTO) -> TaskCost:
        task_cost = TaskCost(**task_dto.to_task_cost())
        self._session.add(task_cost)
        self._session.commit()
        return task_cost
