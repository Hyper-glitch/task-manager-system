from enum import Enum


class TaskProducer(str, Enum):
    TASK_SERVICE = "TASK_SERVICE"


class UserProducer(str, Enum):
    AUTH_SERVICE = "AUTH_SERVICE"
