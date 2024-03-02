from enum import Enum


class UserRoles(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
