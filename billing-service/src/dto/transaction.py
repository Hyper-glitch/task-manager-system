import datetime

from pydantic import BaseModel

from src.dto.task import TaskDTO
from src.dto.user import UserDTO
from src.enums.transaction import TransactionTypes


class TransactionDTO(BaseModel):
    id: int
    public_id: str
    debit: int
    credit: int
    user_id: int
    billing_cycle_id: int
    type: TransactionTypes
    user: UserDTO
    created_at: datetime
    task: TaskDTO | None = None
    task_id: int | None = None
