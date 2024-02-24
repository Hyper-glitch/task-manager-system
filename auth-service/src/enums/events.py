from enum import Enum


class EventTypes(str, Enum):
    BUSINESS_CALL = "BUSINESS_CALL"
    DATA_STREAMING = "DATA_STREAMING"


class EventTitleUser(str, Enum):
    USER_CREATED = "USER.CREATED"
    USER_ROLE_CHANGED = "USER.ROLE_CHANGED"
    USER_DELETED = "USER.DELETED"
