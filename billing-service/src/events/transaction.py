from datetime import datetime

from src.dto.transaction import TransactionDTO


def send_transaction_added_event(transaction_dto: TransactionDTO) -> None:
    event = TransactionAddedEventSchema(
        data={
            "public_id": transaction_dto.public_id,
            "task_public_id": transaction_dto.task and transaction_dto.task.public_id,
            "user_public_id": transaction_dto.user.public_id,
            "debit": transaction_dto.debit,
            "credit": transaction_dto.credit,
            "type": transaction_dto.type,
        },
        produced_at=datetime.utcnow(),
    )
    producer.publish_message(
        event.json().encode("utf-8"),
    )
