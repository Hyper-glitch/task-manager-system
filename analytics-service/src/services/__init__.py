from src.database import db
from src.services.balance import BalanceService
from src.services.task_cost import TaskCostService

balance_service = BalanceService(db.session)
task_cost_service = TaskCostService(db.session)
