from datetime import datetime
from random import randint
from typing import Any

from pydantic import BaseModel

from src.dto.user import UserDTO


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

    def to_task_cost(self) -> dict[str, Any]:
        return {
            "task_id": self.id,
            "title": self.title,
            "description": self.description,
            "credit_cost": randint(20, 40),
            "debit_cost": randint(20, 40),
            "created_at": self.created_at,
        }
