from sqlalchemy.orm import Session

from src.models.account import Account


class AccountRepository:
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def get_accounts(
        self,
        billing_cycle_id: int,
        limit: int,
        offset: int,
        user_id: int | None = None,
    ):
        query = self._session.query(Account).filter(
            Account.billing_cycle_id == billing_cycle_id
        )
        if user_id is not None:
            query = query.filter(Account.user_id == user_id)

        return (
            query.order_by(Account.billing_cycle_id).limit(limit).offset(offset).all()
        )

    def get_acc_balance(
        self,
        billing_cycle_id: int,
        user_id: int | None = None,
    ) -> int:
        query = self._session.query(Account).filter(
            Account.billing_cycle_id == billing_cycle_id
        )
        if user_id is not None:
            query = query.filter(Account.user_id == user_id)

        return query.first().balance
