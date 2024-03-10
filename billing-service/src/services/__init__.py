from src.database import db
from src.kafka.producer import EventsProducer
from src.repositories.account import AccountRepository
from src.repositories.billing import BillingCycleRepository
from src.repositories.task import TaskRepository
from src.repositories.task_cost import TaskCostRepository
from src.repositories.transaction import TransactionRepository
from src.repositories.user import UserRepository
from src.services.account import AccountService
from src.services.billing import BillingCycleService
from src.services.task_event import TaskEventService
from src.services.user_events_service import UserEventService

producer = EventsProducer()

billing_repo = BillingCycleRepository(session=db.session)
billing_service = BillingCycleService(billing_repo=billing_repo, producer=producer)

acc_repo = AccountRepository(session=db.session)
acc_service = AccountService(acc_repo=acc_repo)

task_repo = TaskRepository(session=db.session)

user_repo = UserRepository(session=db.session)
user_event_service = UserEventService(user_repo=user_repo)

task_cost_repo = TaskCostRepository(session=db.session)
transaction_repo = TransactionRepository(session=db.session)

task_event_service = TaskEventService(
    billing_cycle_repo=billing_repo,
    task_repo=task_repo,
    user_repo=user_repo,
    task_cost_repo=task_cost_repo,
    transaction_repo=transaction_repo,
    producer=producer,
)
