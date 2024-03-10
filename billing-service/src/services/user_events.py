import json
import logging
from functools import singledispatch

from pydantic import BaseModel
from schema_registry.models.v1.user_created_event import UserCreatedEventSchema
from schema_registry.models.v1.user_deleted_event import UserDeletedEventSchema
from schema_registry.models.v1.user_role_changed_event import UserRoleChangedEventSchema

from src.config import settings
from src.repositories.user import UserRepository
from src.utils import event_data_fabric

logger = logging.getLogger(settings.project)


class UserEventService:
    USER_EVENTS_MAP = {
        ("USER.CREATED", 1): UserCreatedEventSchema,
        ("USER.ROLE_CHANGED", 1): UserRoleChangedEventSchema,
        ("USER.DELETED", 1): UserDeletedEventSchema,
    }

    def __init__(
        self,
        user_repo: UserRepository,
    ):
        self.user_repo = user_repo

    @staticmethod
    @singledispatch
    def _process_event(event: BaseModel) -> None:
        raise NotImplementedError

    @_process_event.register
    def _delete_user(self, event: UserDeletedEventSchema) -> None:
        public_id = event.data.public_id
        user = self.user_repo.mark_as_deleted(public_id)
        logger.info(f"{user = } deleted")

    @_process_event.register
    def _change_user_role(self, event: UserRoleChangedEventSchema) -> None:
        user = self.user_repo.create_or_update(
            public_id=event.data.public_id, role=event.data.new_role
        )
        logger.info(f"{user = } role changed")

    @_process_event.register
    def _create_user(self, event: UserCreatedEventSchema) -> None:
        data = event.data.dict()
        user = self.user_repo.create_or_update(
            public_id=data.pop("public_id"),
            **data,
        )
        logger.info(f"{user = } user created")

    @classmethod
    def process_user_event_message(cls, message: bytes) -> None:
        event = event_data_fabric(json.loads(message), cls.USER_EVENTS_MAP)
        logger.info(f"Processing event: {event}")
        cls._process_event(event)
