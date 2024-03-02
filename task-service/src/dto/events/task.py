from datetime import datetime

from pydantic import BaseModel, Field, Extra

from src.enums.events import EventTitleTaskCreated
from src.enums.producer import TaskProducer
from src.enums.status import TaskStatus


class UserInfoDTO(BaseModel):
    public_id: str = Field(..., title="Public Id")


class TaskEventDTO(BaseModel, extra=Extra.allow):
    public_id: str = Field(..., title="Public Id")
    title: str = Field(..., title="Title")
    description: str = Field(..., title="Description")
    status: TaskStatus
    assignee: UserInfoDTO
    jira_id: int = Field(None, title="Jira Id")

    class Config:
        from_attributes = True


class TaskCreatedEventDTO(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleTaskCreated = EventTitleTaskCreated.CREATED
    data: TaskEventDTO
    producer: TaskProducer = TaskProducer.TASK_SERVICE


class TaskNewAssigneeDTO(BaseModel):
    public_id: str = Field(..., title="Public Id")
    old_assignee_public_id: str = Field(
        None, title="Old Assignee Public Id"
    )
    new_assignee_public_id: str = Field(..., title="New Assignee Public Id")


class TaskAssignedEventSchema(BaseModel):
    version: int = Field(1, title="Version")
    produced_at: datetime = Field(None, title="Produced At")
    title: EventTitleTaskCreated = EventTitleTaskCreated.ASSIGNED
    data: TaskNewAssigneeDTO
    producer: TaskProducer = TaskProducer.TASK_SERVICE
