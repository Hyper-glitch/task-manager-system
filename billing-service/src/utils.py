from typing import Any, Type

from flask import Response, jsonify
from pydantic import BaseModel


def make_response(code: int, **data) -> Response:
    response: dict[str, Any] = {
        "success": True,
        "code": code,
    }
    if data:
        response["data"] = data
    return jsonify(response)


def event_data_fabric(
    data: dict[str, Any],
    event_map: dict[tuple[str, int], Type[BaseModel]],
) -> BaseModel:
    schema = event_map.get((data.get("title"), data.get("version")))
    if not schema:
        raise ValueError(f"Unknown event: {data}")
    return schema(**data)
