from src.database import db
from src.redis.manager import RedisManager
from src.repositories.user import UserRepository
from src.services.oauth import OAuthService
from src.services.user import UserService

redis_manager = RedisManager()

repository = UserRepository(session=db.session)
user_service = UserService(repository=repository, redis=redis_manager.redis)
oauth_service = OAuthService(repository=repository, redis=redis_manager.redis)
