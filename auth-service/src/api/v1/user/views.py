from http import HTTPStatus

from flask import Response, request

from src.app import app
from src.services import user_service
from src.services.exceptions import UserNotFound, UserAlreadyExists
from src.utils import make_response


@app.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Response:
    try:
        user = user_service.get_user(user_id=user_id)
    except UserNotFound:
        return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
    return make_response(code=200, **user.dict())


@app.route('/', methods=['POST'])
def create_user() -> Response:
    data = request.get_json()
    try:
        user = user_service.create_user(data=data)
    except UserAlreadyExists:
        return Response(status=HTTPStatus.CONFLICT, response="User already exists")
    return make_response(code=200, **user.dict())


@app.route('/<int:user_id>', methods=['PUT'])
def update_user(
        user_id: int,
) -> Response:
    data = request.get_json()
    try:
        user = user_service.change_user_role(user_id=user_id, role=data.role)
    except UserNotFound:
        return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
    return make_response(code=200, **user.dict())


@app.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int) -> Response:
    try:
        user = user_service.delete_user(user_id=user_id)
    except UserNotFound:
        return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
    return make_response(code=204, **user.dict())
