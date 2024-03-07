from src.database import db
from src.repositories.account import AccountRepository
from src.repositories.billing import BillingCycleRepository
from src.services.account import AccountService
from src.services.billing import BillingCycleService

billing_repo = BillingCycleRepository(session=db.session)
billing_service = BillingCycleService(billing_repo=billing_repo)

acc_repo = AccountRepository(session=db.session)
acc_service = AccountService(acc_repo=acc_repo)
