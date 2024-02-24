from src.database import db
from src.dto.api.user import UserAddDTO

from src.dto.events.user import UserRoleChangedEventDTO, UserRoleChangedDataDTO, UserDeletedEventDTO, \
    UserDataDTO, UserCreatedEventDTO
from src.enums.events import EventTypes
from src.enums.roles import UserRoles
from src.events.user import get_producer
from src.models.user import User
from src.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.repository = UserRepository(session=db.session)

    def create_user(self, data: UserAddDTO) -> User:
        user_model = self.repository.create(**data.dict())
        user_dto = UserDataDTO.model_validate(user_model)
        event = UserCreatedEventDTO(data=user_dto)
        producer = get_producer(EventTypes.DATA_STREAMING)
        producer.send(value=event.model_dump(mode="json"))
        return user_model

    def change_user_role(self, user_id: int, role: UserRoles) -> User:
        user = self.repository.get_by_id(user_id, lock=True)
        old_role = user.role
        self.repository.change_role(user=user, role=role)
        event = UserRoleChangedEventDTO(
            data=UserRoleChangedDataDTO(
                public_id=user.public_id,
                old_role=old_role,
                new_role=role,
            )
        )
        producer = get_producer(EventTypes.BUSINESS_CALL)
        producer.send(value=event.model_dump(mode="json"))
        return user

    def delete_user(self, user_id: int) -> User:
        user_obj = self.repository.get_by_id(user_id, lock=True)
        self.repository.delete(user=user_obj)
        user_dto = UserDataDTO.model_validate(user_obj)
        event = UserDeletedEventDTO(data=user_dto)
        producer = get_producer(EventTypes.DATA_STREAMING)
        producer.send(value=event.model_dump(mode="json"))
        return user_obj

    def get_users(self, limit: int, offset: int) -> list[User]:
        users = self.repository.get_users(limit=limit, offset=offset)
        return users

    def count_users(self):
        count = self.repository.count()
        return count

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        return user
