import datetime

from src.config import settings
from src.database import db
from src.dto.api.user import UserAddDTO, UserInfoDTO

from src.dto.events.user import UserRoleChangedEventDTO, UserRoleChangedDataDTO, UserDeletedEventDTO, \
    UserCreatedEventDTO, UserEventDTO
from src.enums.roles import UserRoles
from src.kafka.manager import KafkaManager
from src.models.user import User
from src.repositories.user import UserRepository
from src.services.exceptions import UserNotFound


class UserService:
    def __init__(self):
        self.repository = UserRepository(session=db.session)
        self.kafka = KafkaManager()

    def create_user(self, dto: UserAddDTO) -> UserInfoDTO:
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
