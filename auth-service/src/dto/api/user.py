from uuid import UUID

from pydantic import BaseModel

from src.enums.roles import UserRoles


class UserInfoDTO(BaseModel):
    id: int
    public_id: UUID
    username: str
    email: str
    role: UserRoles

    class Config:
        from_attributes = True


class UserAddDTO(BaseModel):
    username: str
    email: str
    role: UserRoles = UserRoles.EMPLOYEE
    beak_shape: str


class UserUpdateDTO(BaseModel):
    role: UserRoles


class UserPublicIdDTO(BaseModel):
    public_id: str
