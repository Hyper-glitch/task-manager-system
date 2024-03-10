import json
import logging
from functools import singledispatch

from pydantic import BaseModel

from src.config import settings
from src.utils import event_data_fabric
from schema_registry.models.v1.user_created_event import UserCreatedEventSchema

logger = logging.getLogger(settings.project)



class UserEventService:
    USER_EVENTS_MAP = {
        ("USER.CREATED", 1): UserCreatedEventSchema,
        ("USER.ROLE_CHANGED", 1): UserRoleChangedEventSchema,
        ("USER.DELETED", 1): UserDeletedEventSchema,
    }

    @staticmethod
    @singledispatch
    def _process_event(event: BaseModel) -> None:
        raise NotImplementedError

    @staticmethod
    @_process_event.register
    def _delete_user(event: UserDeletedEventSchema) -> None:
        with create_session() as session:
            public_id = event.data.public_id
            user = UserRepo(session).mark_as_deleted(public_id).apply()
            logger.info(f"{user = } deleted")

    @staticmethod
    @_process_event.register
    def _change_user_role(event: UserRoleChangedEventSchema) -> None:
        with create_session() as session:
            user = (
                UserRepo(session)
                .create_or_update(event.data.public_id, role=event.data.new_role)
                .apply()
            )
            logger.info(f"{user = } role changed")

    @staticmethod
    @_process_event.register
    def _create_user(event: UserCreatedEventSchema) -> None:
        with create_session() as session:
            data = event.data.dict()
            public_id = data.pop("public_id")
            user = UserRepo(session).create_or_update(public_id, **data).apply()
            logger.info(f"{user = } user created")

    @classmethod
    def process_user_event_message(cls, message: bytes) -> None:
        event = event_data_fabric(json.loads(message), USER_EVENTS_MAP)
        logger.info(f"Processing event: {event}")
        cls._process_event(event)
