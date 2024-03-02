from pydantic import BaseModel

from src.enums.roles import UserRoles


class UserDTO(BaseModel):
    id: int
    username: str
    role: UserRoles
    public_id: str
    is_deleted: bool
