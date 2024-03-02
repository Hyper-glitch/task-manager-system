from __future__ import annotations

from typing import Any
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.enums.roles import UserRoles
from src.models.user import User


class UserRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_public_id(self, public_id: str):
        return self._session.query(User).filter(User.public_id == public_id).first()

    def get_random_employees(
        self, count: int = 1, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(User)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(
                User.role == UserRoles.EMPLOYEE,
                User.is_deleted.is_(False),
            ).order_by(func.random()).limit(count)
