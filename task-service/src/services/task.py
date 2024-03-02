from src.models.user import User
from src.repositories.task import TaskRepository
from src.services.exceptions import UserNotFound


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_user_by_public_id(self, public_id: str) -> User:
        user = self.repository.get_by_public_id(public_id)
        if not user:
            raise UserNotFound
        return user
