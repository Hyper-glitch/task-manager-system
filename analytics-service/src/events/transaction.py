import logging

from schema_registry.models.v1.transaction_added_event import (
    TransactionAddedEventSchema,
)
from src.repositories.user import TransactionRepository

from src.config import settings

logger = logging.getLogger(settings.project)


class TransactionEventService:
    def __init__(
        self,
        trans_repo: TransactionRepository,
    ):
        self.trans_repo = trans_repo

    def _create_transaction(self, event: TransactionAddedEventSchema) -> None:
        data = event.data.dict()
        trans = self.trans_repo.create(**data)
        logger.info(f"{trans = } created")

    def process_trans_event_message(self, message: bytes) -> None:
        event = TransactionAddedEventSchema.model_validate_json(message)
        logger.info(f"Processing event: {event}")
        self._create_transaction(event)
