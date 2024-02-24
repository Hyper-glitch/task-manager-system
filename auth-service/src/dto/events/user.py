from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    Field,
)

from src.enums.events import EventTitleUser
from src.enums.producer import UserProducer
from src.enums.roles import UserRoles


class UserDataDTO(BaseModel):
    public_id: str = Field(..., title="Public Id")
    username: str = Field(..., title="Username")
    email: str = Field(..., title="Email")
    role: UserRoles


class UserRoleChangedDataDTO(BaseModel):
    public_id: str = Field(..., title="Public Id")
    old_role: Optional[UserRoles] = None
    new_role: UserRoles


class UserCreatedEventDTO(BaseModel):
    version: Optional[int] = Field(1, title="Version")
    produced_at: Optional[datetime] = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_CREATED
    data: UserDataDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE


class UserRoleChangedEventDTO(BaseModel):
    version: Optional[int] = Field(1, title="Version")
    produced_at: Optional[datetime] = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_ROLE_CHANGED
    data: UserRoleChangedDataDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE


class UserDeletedEventDTO(BaseModel):
    version: Optional[int] = Field(1, title="Version")
    produced_at: Optional[datetime] = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_DELETED
    data: UserDataDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE
