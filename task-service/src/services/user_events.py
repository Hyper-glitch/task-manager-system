import json
import logging
from functools import singledispatch

from pydantic import BaseModel

from src.config import settings
from src.dto.events.user import UserCreatedEventDTO, UserDeletedEventDTO, UserRoleChangedEventDTO
from src.repositories.user import UserRepository
from src.utils import event_data_fabric

logger = logging.getLogger(settings.project)

class UserEventService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    @singledispatch
    def _process_event(self, event: BaseModel) -> None:
        raise NotImplementedError

    @_process_event.register
    def _delete_user(self, event: UserDeletedEventDTO) -> None:
        user = self.user_repo.mark_as_deleted(event.data.public_id)
        logger.info(f"{user = } deleted")

    @_process_event.register
    def _change_user_role(self, event: UserRoleChangedEventDTO) -> None:
        user = self.user_repo.create_or_update(event.data.public_id, role=event.data.new_role)
        logger.info(f"{user = } role changed")

    @_process_event.register
    def _create_user(self, event: UserCreatedEventDTO) -> None:
        data = event.data.dict()
        public_id = data.pop("public_id")
        user = self.user_repo.create_or_update(public_id, **data)
        logger.info(f"{user = } user created")

    def process_user_event_message(self, message: bytes) -> None:
        event = event_data_fabric(json.loads(message))
        logger.info(f"Processing event: {event}")
        self._process_event(event=event)