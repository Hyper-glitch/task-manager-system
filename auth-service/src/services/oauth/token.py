from collections import namedtuple
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.enums.roles import UserRoles


class Token(BaseModel):
    public_id: UUID
    username: str
    email: str
    role: UserRoles
    scopes: list[str]
    exp: datetime | None = None


TokenPair = namedtuple("TokenPair", ["access_token", "refresh_token"])
