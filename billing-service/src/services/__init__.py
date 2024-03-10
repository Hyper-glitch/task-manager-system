from src.database import db
from src.kafka.producer import EventsProducer
from src.repositories.account import AccountRepository
from src.repositories.billing import BillingCycleRepository
from src.repositories.user import UserRepository
from src.services.account import AccountService
from src.services.billing import BillingCycleService
from src.services.user_events_service import UserEventService

producer = EventsProducer()

billing_repo = BillingCycleRepository(session=db.session)
billing_service = BillingCycleService(billing_repo=billing_repo, producer=producer)

acc_repo = AccountRepository(session=db.session)
acc_service = AccountService(acc_repo=acc_repo)

user_repo = UserRepository(session=db.session)
user_event_service = UserEventService(user_repo=user_repo)
