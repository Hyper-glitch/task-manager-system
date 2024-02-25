from http import HTTPStatus

from flask import Response
from flask_restx import Resource, reqparse

from src.dto.api.user import UserAddDTO
from src.services import user_service
from src.services.exceptions import UserNotFound, UserAlreadyExists
from src.utils import make_response


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('email', type=str)
    parser.add_argument('role', type=str)
    parser.add_argument('beak_shape', type=str)
    parser.add_argument('user_id', type=str)

    def get(self) -> Response:
        data = User.parser.parse_args()
        try:
            user_dto = user_service.get_user(user_id=data["user_id"])
        except UserNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
        else:
            return make_response(code=200, **user_dto.model_dump())

    def post(self) -> Response:
        data = User.parser.parse_args()
        try:
            dto = UserAddDTO.model_validate(data)
            user_dto = user_service.create_user(dto=dto)
        except UserAlreadyExists:
            return Response(status=HTTPStatus.CONFLICT, response="User already exists")
        except Exception as exc:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=str(exc))
        else:
            return make_response(code=200, **user_dto.model_dump())

    def put(self) -> Response:
        data = User.parser.parse_args()
        try:
            user_dto = user_service.change_user_role(user_id=data["user_id"], role=data["role"])
        except UserNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
        except Exception as exc:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=str(exc))
        return make_response(code=200, **user_dto.model_dump())

    def delete(self) -> Response:
        data = User.parser.parse_args()
        try:
            user_dto = user_service.delete_user(user_id=data["user_id"])
        except UserNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="User not found")
        except Exception as exc:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=str(exc))
        return make_response(code=204, **user_dto.model_dump())
