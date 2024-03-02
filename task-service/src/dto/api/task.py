from datetime import datetime

from pydantic import BaseModel

from src.dto.api.user import UserDTO
from src.enums.status import TaskStatus


class TaskDTO(BaseModel):
    id: int
    public_id: str
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee_id: int
    assignee: UserDTO | None
