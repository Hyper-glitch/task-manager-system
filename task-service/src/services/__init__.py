from src.database import db
from src.kafka.manager import KafkaManager
from src.repositories.task import TaskRepository
from src.repositories.user import UserRepository
from src.services.task import TaskService
from src.services.user import UserService
from src.services.user_events import UserEventService

kafka = KafkaManager()

user_repo = UserRepository(session=db.session)
user_service = UserService(repository=user_repo)

task_repo = TaskRepository(session=db.session)
task_service = TaskService(task_repo=task_repo, user_repo=user_repo, kafka=kafka)

user_event_service = UserEventService(user_repo=user_repo)
