from src.database import db
from src.repositories.billing import BillingCycleRepository
from src.services.billing import BillingCycleService

billing_repo = BillingCycleRepository(session=db.session)
billing_service = BillingCycleService(billing_repo=billing_repo)
