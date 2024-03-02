from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "OPEN"
    DONE = "DONE"
