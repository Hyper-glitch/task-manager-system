import datetime
from typing import Any

import jwt
from jwt import PyJWTError
from redis import Redis

from src.config import settings
from src.dto.api.user import UserAddDTO, UserInfoDTO
from src.dto.events.user import UserRoleChangedEventDTO, UserRoleChangedDataDTO, UserDeletedEventDTO, \
    UserCreatedEventDTO, UserEventDTO, UserUpdatedEventDTO
from src.enums.roles import UserRoles
from src.kafka.manager import KafkaManager
from src.models.user import User
from src.repositories.user import UserRepository
from src.services.exceptions import UserNotFound, AuthorizationCodeInvalid, InvalidTokenException


class UserService:
    def __init__(self, repository: UserRepository, redis: Redis):
        self.repository = repository
        self.kafka = KafkaManager()
        self.redis = redis

    def create_user(self, data: dict[str, Any]) -> UserInfoDTO:
        dto = UserAddDTO.model_validate(data)
        user = self.repository.create(dto=dto)
        event = UserCreatedEventDTO(data=UserEventDTO.from_orm(user), produced_at=datetime.datetime.now())
        self.kafka.send(value=event.model_dump(mode="json"), topic=settings.data_streaming_topic)
        user_dto = UserInfoDTO.from_orm(user)
        return user_dto

    def change_user_role(self, user_id: int, role: UserRoles) -> UserInfoDTO:
        user = self.repository.get_by_id(user_id, lock=True)
        if not user:
            raise UserNotFound

        old_role = user.role
        self.repository.change_role(user=user, role=role)

        event = UserUpdatedEventDTO(data=UserEventDTO.from_orm(user), produced_at=datetime.datetime.now())
        self.kafka.send(value=event.model_dump(mode="json"), topic=settings.data_streaming_topic)

        if role != old_role:
            event = UserRoleChangedEventDTO(
                data=UserRoleChangedDataDTO(
                    public_id=user.public_id,
                    old_role=old_role,
                    new_role=role,
                ),
                produced_at=datetime.datetime.now(),
            )
            self.kafka.send(value=event.model_dump(mode="json"), topic=settings.business_event_topic)

        user_dto = UserInfoDTO.from_orm(user)
        return user_dto

    def delete_user(self, user_id: int) -> UserInfoDTO:
        user = self.repository.get_by_id(user_id, lock=True)
        if not user:
            raise UserNotFound

        self.repository.delete(user=user)
        event = UserDeletedEventDTO(data=UserEventDTO.from_orm(user), produced_at=datetime.datetime.now())
        self.kafka.send(value=event.model_dump(mode="json"), topic=settings.data_streaming_topic)
        user_dto = UserInfoDTO.from_orm(user)
        return user_dto

    def get_users(self, limit: int, offset: int) -> list[User]:
        users = self.repository.get_users(limit=limit, offset=offset)
        return users

    def count_users(self):
        count = self.repository.count()
        return count

    def get_user(self, user_id: int) -> UserInfoDTO:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFound

        user_dto = UserInfoDTO.from_orm(user)
        return user_dto

    def identify_user_by_beak_shape(self, beak_shape: str) -> UserInfoDTO:
        user = self.repository.get_by_beak_shape(beak_shape)
        if not user:
            raise UserNotFound

        user_dto = UserInfoDTO.from_orm(user)
        return user_dto

    def identify_user_by_auth_code(self, code: str) -> User:
        user_id = self.redis.get(f"user.auth_code.{code}")
        if not user_id:
            raise AuthorizationCodeInvalid("Invalid authentication code")

        user = self.repository.get_by_id(user_id=int(user_id))
        if not user:
            raise UserNotFound(f"User with id {user_id} not found")

        return user

    def identify_user_by_refresh_token(self, refresh_token: str) -> User:
        try:
            token_payload = jwt.decode(
                refresh_token, settings.public_key, algorithms="RS256"
            )
        except PyJWTError:
            raise InvalidTokenException("Invalid token")

        public_id = token_payload.get("public_id", "")
        if not public_id:
            raise InvalidTokenException("Invalid token data")

        user = self.repository.get_by_public_id(public_id=public_id)
        if not user:
            raise UserNotFound(f"User with public_id {public_id} not found")

        return user
