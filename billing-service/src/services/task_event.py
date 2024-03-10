import json
import logging
from datetime import datetime
from functools import singledispatch

from pydantic import BaseModel
from schema_registry.models.v1.task_assigned_event import TaskAssignedEventSchema
from schema_registry.models.v1.task_completed_event import TaskCompletedEventSchema
from schema_registry.models.v1.task_cost_added_event import TaskCostAddedDataSchema
from schema_registry.models.v1.task_cost_added_event import TaskCostAddedEventSchema
from schema_registry.models.v1.transaction_added_event import TransactionAddedEventSchema
from schema_registry.models.v2.task_created_event import TaskCreatedEventSchema

from src.config import settings
from src.database import db
from src.dto.task import TaskDTO
from src.dto.transaction import TransactionDTO
from src.enums.transaction import TransactionTypes
from src.kafka.producer import EventsProducer
from src.repositories.billing import BillingCycleRepository
from src.repositories.task import TaskRepository
from src.repositories.task_cost import TaskCostRepository
from src.repositories.transaction import TransactionRepository
from src.repositories.user import UserRepository
from src.utils import event_data_fabric

logger = logging.getLogger(settings.project)


class TaskEventService:
    TASK_EVENTS_MAP = {
        ("TASK.ASSIGNED", 1): TaskAssignedEventSchema,
        ("TASK.COMPLETED", 1): TaskCompletedEventSchema,
        ("TASK.CREATED", 2): TaskCreatedEventSchema,
    }

    def __init__(
            self,
            billing_cycle_repo: BillingCycleRepository,
            task_repo: TaskRepository,
            user_repo: UserRepository,
            task_cost_repo: TaskCostRepository,
            transaction_repo: TransactionRepository,
            producer: EventsProducer,
    ):
        self.billing_cycle_repo = billing_cycle_repo
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.task_cost_repo = task_cost_repo
        self.transaction_repo = transaction_repo
        self.producer = producer

    @staticmethod
    @singledispatch
    def _process_event(event: BaseModel) -> None:
        raise NotImplementedError

    @_process_event.register
    def create_task(self, event: TaskCreatedEventSchema) -> None:
        task_dto = TaskDTO.from_orm(event.data)
        task_cost = self.task_cost_repo.get_by_task_id(task_id=task_dto.id)
        if not task_cost:
            task_cost = self.task_cost_repo.add(task_dto=task_dto)
            task_cost_event = TaskCostAddedEventSchema(
                public_id=task_cost.public_id,
                task_public_id=task_dto.public_id,
                debit_cost=task_cost.debit_cost,
                credit_cost=task_cost.credit_cost,
            )
            self.producer.send(value=task_cost_event.model_dump_json(), topic="tasks-cost")

    @_process_event.register
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
            data = TaskCostAddedDataSchema(
                public_id=task_cost.public_id,
                task_public_id=task.public_id,
                debit_cost=task_cost.debit_cost,
                credit_cost=task_cost.credit_cost,
            )
            task_cost_event = TaskCostAddedEventSchema(
                data=data,
                produced_at=datetime.utcnow(),
            )
            self.producer.send(value=task_cost_event.model_dump_json(), topic="tasks-cost")

        transaction_event = TransactionAddedEventSchema(
            data=transaction_dto,
            produced_at=datetime.utcnow(),
        )
        self.producer.send(value=transaction_event.model_dump_json(), topic="transactions")

    @_process_event.register
    def complete_task(self, event: TaskCompletedEventSchema) -> None:
        task_cost_added = False

        with db.session.begin():
            billing_cycle = self.billing_cycle_repo.get_last(lock=True)
            task = self.task_repo.get_or_create(public_id=event.data.public_id)
            user = self.user_repo.create_or_update(public_id=event.data.assignee_public_id)

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
            data = TaskCostAddedDataSchema(
                public_id=task_cost.public_id,
                task_public_id=task.public_id,
                debit_cost=task_cost.debit_cost,
                credit_cost=task_cost.credit_cost,
            )
            task_cost_event = TaskCostAddedEventSchema(
                data=data,
                produced_at=datetime.utcnow(),
            )
            self.producer.send(value=task_cost_event.model_dump_json(), topic="tasks-cost")

        transaction_event = TransactionAddedEventSchema(
            data=transaction_dto,
            produced_at=datetime.utcnow(),
        )
        self.producer.send(value=transaction_event.model_dump_json(), topic="transactions")

    @classmethod
    def process_task_event_message(cls, message: bytes) -> None:
        event = event_data_fabric(json.loads(message), cls.TASK_EVENTS_MAP)
        logger.info(f"Processing event: {event}")
        cls._process_event(event=event)
