import logging

from src.config import settings
from src.database import db
from src.dto.task import TaskDTO
from src.dto.transaction import TransactionDTO
from src.enums.transaction import TransactionTypes
from src.events.task_cost import send_task_cost_added_event
from src.events.transaction import send_transaction_added_event
from src.repositories.billing import BillingCycleRepository
from src.repositories.task import TaskRepository
from src.repositories.task_cost import TaskCostRepository
from src.repositories.user import UserRepository

logger = logging.getLogger(settings.project)


class TaskEventService:
    def __init__(
        self,
        billing_cycle_repo: BillingCycleRepository,
        task_repo: TaskRepository,
        user_repo: UserRepository,
        task_cost_repo: TaskCostRepository,
        transaction_repo,
        broker,
    ):
        self.billing_cycle_repo = billing_cycle_repo
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.task_cost_repo = task_cost_repo
        self.transaction_repo = transaction_repo
        self.broker = broker

    def create_task(self, event: TaskCreatedEventSchema) -> None:
        task_dto = TaskDTO.from_orm(event.data)
        task_cost = self.task_cost_repo.get_by_task_id(task_id=task_dto.id)
        if not task_cost:
            task_cost = self.task_cost_repo.add(task_dto=task_dto)
            send_task_cost_added_event(
                task_cost=task_cost, task_public_id=task_dto.public_id
            )

    def assign_task(self, event: TaskAssignedEventSchema) -> None:
        task_dto = TaskDTO.from_orm(event.data)
        is_task_cost_added = False

        with db.session.begin():
            billing_cycle = self.billing_cycle_repo.get_last(lock=True)
            task = self.task_repo.get_by_public_id(public_id=task_dto.public_id)
            user = self.user_repo.get_by_public_id(
                public_id=event.data.new_assignee_public_id
            )

            task_cost = self.task_cost_repo.get_by_task_id(task_id=task.id)
            if not task_cost:
                task_cost = self.task_cost_repo.add(task_dto=task_dto)
                is_task_cost_added = True

            transaction = self.transaction_repo.add(
                debit=task_cost.debit_cost,
                task_id=task.id,
                user_id=user.id,
                billing_cycle_id=billing_cycle.id,
                type=TransactionTypes.EXPENSE,
            )
            transaction_dto = TransactionDTO.from_orm(transaction)

        if is_task_cost_added:
            send_task_cost_added_event(
                task_cost=task_cost, task_public_id=task_dto.public_id
            )
        send_transaction_added_event(transaction_dto)

    def complete_task(self, event: TaskCompletedEventSchema) -> None:
        task_cost_added = False

        with db.session.begin():
            billing_cycle = self.billing_cycle_repo.get_last(lock=True)
            task = self.task_repo.get_or_create(public_id=event.data.public_id)
            user = self.user_repo.get_or_create(public_id=event.data.assignee_public_id)

            task_cost = self.task_cost_repo.get_by_task_id(task.id)
            if not task_cost:
                task_cost = self.task_cost_repo.add(task.id)
                task_cost_added = True

            transaction = self.transaction_repo.add(
                credit=task_cost.credit_cost,
                task_id=task.id,
                user_id=user.id,
                billing_cycle_id=billing_cycle.id,
                type=TransactionTypes.INCOME,
            )
            transaction_dto = TransactionDTO.from_orm(transaction)

        if task_cost_added:
            send_task_cost_added_event(
                task_cost=task_cost, task_public_id=task.public_id
            )
        send_transaction_added_event(transaction_dto=transaction_dto)
