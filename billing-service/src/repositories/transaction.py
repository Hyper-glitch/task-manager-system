from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.transaction import Transaction


class TransactionRepository:
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

    def get_balance_by_cycle(
        self, user_id: int, billing_cycle_id: int
    ) -> tuple[int, int]:
        result = (
            self._session.query(
                func.sum(Transaction.debit).label("debit"),
                func.sum(Transaction.credit).label("credit"),
            )
            .filter(
                Transaction.billing_cycle_id == billing_cycle_id,
                Transaction.user_id == user_id,
            )
            .all()
        )
        if result:
            return result[0]["debit"], result[0]["credit"]
        return 0, 0
