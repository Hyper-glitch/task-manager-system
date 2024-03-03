from enum import Enum


class EventTitleTaskCreated(str, Enum):
    CREATED = "TASK.CREATED"
    ASSIGNED = "TASK.ASSIGNED"
    COMPLETED = "TASK.COMPLETED"


class EventTitleUser(str, Enum):
    USER_CREATED = "USER.CREATED"
    USER_ROLE_CHANGED = "USER.ROLE_CHANGED"
    USER_DELETED = "USER.DELETED"
    USER_UPDATED = "USER.UPDATED"
