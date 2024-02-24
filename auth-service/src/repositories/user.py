from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from src.enums.roles import UserRoles
from src.models.user import User


class UserRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_beak_shape(self, beak_shape: str):
        return self._session.query(User).filter(User.beak_shape == beak_shape).first()

    def get_by_id(
            self, user_id: int, lock: bool = False, **lock_params: Any
    ):
        query = self._session.query(User)
        if lock:
            query = query.with_for_update(**lock_params)
        return query.filter(User.id == user_id).first()

    def get_by_public_id(self, public_id: str):
        return self._session.query(User).filter(User.public_id == public_id).first()

    def create(self, **data: Any) -> User:
        user = User(**data)
        self._session.add(user)
        self._session.commit()
        return user

    def change_role(self, user: User, role: UserRoles):
        user.role = role
        self._session.commit()

    def delete(self, user: User):
        self._session.delete(user)
        self._session.commit()

    def count(self) -> int:
        return self._session.query(User).count()

    def get_users(self, offset: int, limit: int):
        return self._session.query(User).order_by(User.id).offset(offset).limit(limit).all()
