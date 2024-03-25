from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.models.transaction import Transaction


class BalanceService:
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def get_today_manager_balance(self):
        start_day = datetime.combine(date.today(), datetime.min.time())
        end_day = datetime.combine(date.today(), datetime.max.time())
        transactions = (
            self._session.query(Transaction)
            .filter(Transaction.created_at.between(start_day, end_day))
            .all()
        )
        return {
            "managers_income": sum(
                transaction.debit - transaction.credit for transaction in transactions
            )
        }

    def get_worker_statuses(self):
        start_day = datetime.combine(date.today(), datetime.min.time())
        end_day = datetime.combine(date.today(), datetime.max.time())
        transactions = (
            self._session.query(
                Transaction.user.public_id,
                func.sum(Transaction.debit),
                func.sum(Transaction.credit),
            )
            .filter(Transaction.created_at.between(start_day, end_day))
            .group_by(Transaction.user.public_id)
            .all()
        )
        return {
            "negative_balances_amount": sum(
                (trans.debit - trans.credit < 0) for trans in transactions
            ),
            "positive_balances_amount": sum(
                (trans.debit - trans.credit > 0) for trans in transactions
            ),
        }
