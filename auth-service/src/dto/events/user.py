from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    Field, Extra,
)

from src.enums.events import EventTitleUser
from src.enums.producer import UserProducer
from src.enums.roles import UserRoles


class UserEventDTO(BaseModel, extra=Extra.allow):
    public_id: UUID = Field(..., title="Public Id")
    username: str = Field(..., title="Username")
    email: str = Field(..., title="Email")
    role: UserRoles

    class Config:
        from_attributes = True


class UserRoleChangedDataDTO(BaseModel):
    public_id: UUID = Field(..., title="Public Id")
    old_role: Optional[UserRoles] = None
    new_role: UserRoles


class UserCreatedEventDTO(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_CREATED
    data: UserEventDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE


class UserUpdatedEventDTO(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_UPDATED
    data: UserEventDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE


class UserRoleChangedEventDTO(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_ROLE_CHANGED
    data: UserRoleChangedDataDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE


class UserDeletedEventDTO(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleUser = EventTitleUser.USER_DELETED
    data: UserEventDTO
    producer: UserProducer = UserProducer.AUTH_SERVICE
