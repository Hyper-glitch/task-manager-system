from src.database import db
from src.repositories.user import UserRepository
from src.services.oauth import OAuthService
from src.services.user import UserService

repository = UserRepository(session=db.session)
user_service = UserService(repository=repository)
oauth_service = OAuthService(repository=repository)
