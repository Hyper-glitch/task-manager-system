from src.models.account import Account
from src.repositories.account import AccountRepository


class AccountService:
    def __init__(self, acc_repo: AccountRepository):
        self.acc_repo = acc_repo

    def get_balances(
            self,
            billing_cycle_id: int,
            user_id: int,
            limit: int,
            offset: int,
    ) -> list[Account]:
        return self.acc_repo.get_accounts(
                billing_cycle_id=billing_cycle_id,
                user_id=user_id,
                limit=limit,
                offset=offset,
            )

    def get_acc_balance(self, billing_cycle_id: int, user_id: int) -> int:
        return self.acc_repo.get_acc_balance(
            billing_cycle_id=billing_cycle_id,
            user_id=user_id,
        )
