from typing import Any

from flask import Response, jsonify
import jwt

from src.config import settings


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
