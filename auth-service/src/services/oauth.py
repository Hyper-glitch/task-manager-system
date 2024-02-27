from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from redis import Redis

from src.config import settings
from src.constants import ROLES_SCOPE_MAP
from src.models.user import User
from src.repositories.user_token import UserRefreshTokenRepo
from src.structures.token import Token, TokenPair


class OAuthService:
    def __init__(self, repository: UserRefreshTokenRepo, redis: Redis):
        self.repository = repository
        self.redis = redis

    def generate_auth_code(self, user_id: str) -> str:
        auth_code = uuid4().hex
        self.redis.set(
            f"user.auth_code.{auth_code}", user_id, ex=settings.auth_code_expiration
        )
        return auth_code

    @staticmethod
    def generate_token(token_data: Token, expires_delta: int) -> str:
        token_data.exp = datetime.utcnow() + timedelta(expires_delta)
        token = jwt.encode(
            token_data,
            settings.secret_key,
            algorithm="RS256",
        )
        return token

    def create_token(self, user: User) -> TokenPair:
        token_data = Token(
            public_id=user.public_id,
            username=user.username,
            email=user.email,
            role=user.role,
            scopes=ROLES_SCOPE_MAP.get(user.role, [])
        )
        access_token = self.generate_token(
            token_data=token_data, expires_delta=settings.access_token_expiration
        )
        refresh_token = self.generate_token(
            token_data=token_data, expires_delta=settings.refresh_token_expiration
        )
        self.repository.upsert_refresh_token(user.id, refresh_token)
        return TokenPair(access_token, refresh_token)
