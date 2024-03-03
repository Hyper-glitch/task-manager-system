from typing import Any

from flask import Response, jsonify
import jwt

from src.config import settings
from src.dto.events.user import UserCreatedEventDTO, UserRoleChangedEventDTO, UserDeletedEventDTO

USER_EVENTS_MAP = {
    ("USER.CREATED", 1): UserCreatedEventDTO,
    ("USER.ROLE_CHANGED", 1): UserRoleChangedEventDTO,
    ("USER.DELETED", 1): UserDeletedEventDTO,
}


def decode_token(token: str) -> dict[str, Any]:
    token = token.replace("Bearer ", "")
    token_payload: dict[str, Any] = jwt.decode(
        token,
        settings.public_key,
        algorithms=[settings.token_algorithm],
    )
    return token_payload


def make_response(code: int, **data) -> Response:
    response: dict[str, Any] = {
        "success": True,
        "code": code,
    }
    if data:
        response["data"] = data
    return jsonify(response)


def event_data_fabric(data: dict[str, Any]) -> Any:
    title = data.get("title")
    version = data.get("version")
    schema = USER_EVENTS_MAP.get((title, version))

    if not schema:
        raise ValueError(f"Unknown event: {data}")

    return schema(**data)
