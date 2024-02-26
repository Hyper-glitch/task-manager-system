from enum import Enum


class GrantType(str, Enum):
    AUTHORIZATION_CODE = "AUTHORIZATION_CODE"
    REFRESH_TOKEN = "REFRESH_TOKEN"
