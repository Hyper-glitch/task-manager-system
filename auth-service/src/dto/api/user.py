from pydantic import BaseModel

from src.enums.roles import UserRoles


class UserInfoDTO(BaseModel):
    id: int
    public_id: str
    username: str
    email: str
    role: UserRoles


class UserAddDTO(BaseModel):
    username: str
    email: str
    role: UserRoles = UserRoles.EMPLOYEE
    beak_shape: str


class UserUpdateDTO(BaseModel):
    role: UserRoles


class UserPublicIdDTO(BaseModel):
    public_id: str
