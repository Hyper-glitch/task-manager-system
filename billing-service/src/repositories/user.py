import enum
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.models.user import User


class UserRepository:
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ) -> User | None:
        query = self._session.query(User)
        if lock:
            query = query.with_for_update(**lock_params)

        return query.filter(User.id == id_).first()

    def get_by_public_id(self, public_id: str, lock: bool = False, **lock_params: Any):
        query = self._session.query(User)
        if lock:
            query = query.with_for_update(**lock_params)

        return query.filter(User.public_id == public_id).first()

    def mark_as_deleted(self, public_id: str) -> User | None:
        user = self.get_by_public_id(public_id, lock=True)
        if user:
            user.is_deleted = True
            self._session.add(user)
        return user

    def create_or_update(self, public_id: str, **data: Any):
        user = self.get_by_public_id(public_id, lock=True)
        if not user:
            self._session.execute(
                insert(User)
                .values(public_id=public_id)
                .on_conflict_do_nothing(
                    index_elements=["public_id"],
                )
            )
            user = self.get_by_public_id(public_id, lock=True)

        if not user.is_deleted:
            for key, value in data.items():
                if key in User.get_updatable_fields():
                    old_value = getattr(user, key)

                    if isinstance(old_value, enum.Enum):
                        old_value = old_value.value

                    if isinstance(value, enum.Enum):
                        value = value.value

                    if old_value != value:
                        setattr(user, key, value)

            self._session.add(user)
        return user
