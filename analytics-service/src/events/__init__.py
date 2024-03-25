from src.database import db
from src.events.user_events import UserEventService

from src.events.task_cost import TaskCostEventService
from src.events.transaction import TransactionEventService

user_repo = UserRepository(db.session)
user_events_service = UserEventService(user_repo=user_repo)

task_cost_repo = TaskCostRepository(db.session)
task_cost_events_service = TaskCostEventService(task_cost_repo=task_cost_repo)

trans_repo = TransactionRepository(db.session)
trans_events_service = TransactionEventService(trans_repo=trans_repo)
