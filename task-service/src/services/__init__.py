from src.database import db
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository
from src.services.task import TaskService
from src.services.user import UserService


user_repo = UserRepository(session=db.session)
user_service = UserService(repository=user_repo)

task_repo = TaskRepository(session=db.session)
task_service = TaskService(repository=task_repo)
