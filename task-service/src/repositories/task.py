from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.models.task import Task
from src.models.user import User


class TaskRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_public_id(
            self, public_id: str, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(Task, User)

        if lock:
            query = query.with_for_update(**lock_params)

        return query.filter(Task.public_id == public_id).first()
