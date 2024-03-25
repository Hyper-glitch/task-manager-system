import logging

from schema_registry.models.v1.user_created_event import UserCreatedEventSchema
from src.repositories.user import UserRepository

from src.config import settings

logger = logging.getLogger(settings.project)


class UserEventService:
    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    def _create_user(self, event: UserCreatedEventSchema) -> None:
        data = event.data.dict()
        user = self.user_repo.create(**data)
        logger.info(f"{user = } user created")

    def process_user_event_message(self, message: bytes) -> None:
        event = UserCreatedEventSchema.model_validate_json(message)
        logger.info(f"Processing event: {event}")
        self._create_user(event)
