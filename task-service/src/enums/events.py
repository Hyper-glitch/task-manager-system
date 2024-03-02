from enum import Enum


class EventTitleTaskCreated(str, Enum):
    CREATED = "TASK.CREATED"
    ASSIGNED = "TASK.ASSIGNED"
    COMPLETED = "TASK.COMPLETED"
