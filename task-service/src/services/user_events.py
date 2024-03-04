import logging

from src.config import settings
from src.dto.events.user import UserCreatedEventDTO, UserDeletedEventDTO, UserRoleChangedEventDTO
from src.kafka.broker import broker
from src.repositories.user import UserRepository

logger = logging.getLogger(settings.project)


class UserEventService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @broker.subscriber("users-stream")
    def _delete_user(self, event: UserDeletedEventDTO) -> None:
        user = self.user_repo.mark_as_deleted(event.data.public_id)
        logger.info(f"{user = } deleted")

    @broker.subscriber("users-stream")
    def _change_user_role(self, event: UserRoleChangedEventDTO) -> None:
        user = self.user_repo.create_or_update(event.data.public_id, role=event.data.new_role)
        logger.info(f"{user = } role changed")

    @broker.subscriber("users-stream")
    def _create_user(self, event: UserCreatedEventDTO) -> None:
        data = event.data.dict()
        public_id = data.pop("public_id")
        user = self.user_repo.create_or_update(public_id, **data)
        logger.info(f"{user = } user created")
