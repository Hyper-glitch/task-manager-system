from __future__ import annotations

from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


class TaskRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(Task)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(Task.id == id_).first()

    def get_by_public_id(
        self, public_id: str, lock: bool = False, **lock_params: Any
    ) -> Task | None:
        query = self._session.query(Task)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(Task.public_id == public_id).first()

    def get_or_create(self, public_id: str) -> Task:
        task = self.get_by_public_id(public_id=public_id, lock=True)
        if not task:
            task = self._session.execute(
                insert(Task)
                .values(public_id=public_id)
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )
        return task
