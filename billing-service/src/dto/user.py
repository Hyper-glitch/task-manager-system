from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    username: str
    role: UserRoles
    public_id: str
    is_deleted: bool
