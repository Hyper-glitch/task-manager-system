from src.enums.permissions import Permissions
from src.enums.roles import UserRoles

ROLES_SCOPE_MAP = {
    UserRoles.EMPLOYEE: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
    ],
    UserRoles.ADMIN: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
        Permissions.CAN_ASSIGN_NEW_TASKS.value,
    ],
    UserRoles.MANAGER: [
        Permissions.CAN_READ_USERS.value,
        Permissions.CAN_UPDATE_USER.value,
        Permissions.CAN_READ_SELF_TASKS.value,
        Permissions.CAN_READ_ALL_TASKS.value,
        Permissions.CAN_UPDATE_SELF_TASKS.value,
        Permissions.CAN_ASSIGN_NEW_TASKS.value,
    ],
}
