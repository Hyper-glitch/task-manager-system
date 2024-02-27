from __future__ import annotations

from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from src.models.user import UserRefreshToken


class UserRefreshTokenRepo:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_user_by_id(
        self, user_id: int, lock: bool = False, **lock_params: Any
    ) -> UserRefreshToken | None:
        query = self._session.query(UserRefreshToken)

        if lock:
            query = query.with_for_update(**lock_params)

        user_refresh_token = query.filter(
            UserRefreshToken.user_id == user_id
        ).first()
        return user_refresh_token

    def upsert_refresh_token(
        self, user_id: int, refresh_token: str
    ) -> None:
        user_refresh_token = self.get_user_by_id(user_id=user_id, lock=True).context()
        if not user_refresh_token:
            self._session.execute(
                insert(UserRefreshToken)
                .values(user_id=user_id, refresh_token=refresh_token)
                .on_conflict_do_update(
                    index_elements=["user_id"],
                    set_={"refresh_token": refresh_token},
                )
            )
        else:
            user_refresh_token.refresh_token = refresh_token
            self._session.commit()
