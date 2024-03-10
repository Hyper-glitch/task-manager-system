from datetime import datetime

from schema_registry.models.v1.transaction_added_event import (
    TransactionAddedEventSchema,
)

from src.dto.transaction import TransactionDTO
from src.enums.transaction import TransactionTypes
from src.kafka.producer import EventsProducer
from src.notification.sender import send_email_notification
from src.repositories.billing import BillingCycleRepository
from src.repositories.transaction import TransactionRepository


class PaymentService:
    def __init__(
            self,
            transaction_repo: TransactionRepository,
            billing_repo: BillingCycleRepository,
            producer: EventsProducer,
    ):
        self.transaction_repo = transaction_repo
        self.billing_repo = billing_repo
        self.producer = producer

    def send_payment(self, user_id: int, billing_cycle_id: int):
        debit, credit = self.transaction_repo.get_balance_by_cycle(
            user_id=user_id,
            billing_cycle_id=billing_cycle_id,
        )

        payment = credit + debit

        new_billing_cycle = self.billing_repo.get_last()
        if payment <= 0:
            transaction = (
                self.transaction_repo
                .add(
                    debit=payment,
                    type=TransactionTypes.PAYMENT,
                    billing_cycle_id=new_billing_cycle.id,
                    user_id=user_id,
                )
            )
            dto = TransactionDTO.from_orm(transaction)
        else:
            transaction = (
                self.transaction_repo
                .add(
                    credit=payment,
                    type=TransactionTypes.PAYMENT,
                    billing_cycle_id=new_billing_cycle.id,
                    user_id=user_id,
                )
            )
            dto = TransactionDTO.from_orm(transaction)
            send_email_notification(dto)

        transaction_event = TransactionAddedEventSchema(
            data=dto,
            produced_at=datetime.utcnow(),
        )
        self.producer.send(
            value=transaction_event.model_dump_json(), topic="transactions"
        )
