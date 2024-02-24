from typing import Any

from flask import Response, jsonify


def make_response(code: int, **data) -> Response:
    response: dict[str, Any] = {
        "success": True,
        "code": code,
    }
    if data:
        response["data"] = data
    return jsonify(response)
