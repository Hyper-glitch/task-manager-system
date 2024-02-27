from src.database import db
from src.redis.manager import RedisManager
from src.repositories.user import UserRepository
from src.repositories.user_token import UserRefreshTokenRepo
from src.services.oauth.oauth import OAuthService
from src.services.user import UserService

redis_manager = RedisManager()

user_repo = UserRepository(session=db.session)
user_refresh_token_repo = UserRefreshTokenRepo(session=db.session)
user_service = UserService(repository=user_repo, redis=redis_manager.redis)
oauth_service = OAuthService(repository=user_refresh_token_repo, redis=redis_manager.redis)
