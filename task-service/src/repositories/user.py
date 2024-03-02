from __future__ import annotations

from sqlalchemy.orm import Session

from src.models.user import User


class UserRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_public_id(self, public_id: str):
        return self._session.query(User).filter(User.public_id == public_id).first()
