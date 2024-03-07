from typing import Any

from sqlalchemy.orm import Session

from src.models.transaction import Transaction


class TransactionRepo:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_id(
        self, id_: int, lock: bool = False, **lock_params: Any
    ) -> Transaction | None:
        query = self._session.query(Transaction)
        if lock:
            query = query.with_for_update(**lock_params)

        transaction = query.filter(Transaction.id == id_).first()
        return transaction

    def add(self, **data: Any) -> Transaction:
        transaction = Transaction(**data)
        self._session.add(transaction)
        self._session.commit()
        return transaction
