from http import HTTPStatus

from flask import Response
from flask_restx import Resource, reqparse
from jwt import PyJWTError

from src.services import user_service
from src.services.exceptions import UserNotFound
from src.utils import decode_token, make_response


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('token', type=str)

    def get(self) -> Response:
        data = User.parser.parse_args()
        try:
            token = decode_token(token=data["token"])
        except PyJWTError:
            return Response(status=HTTPStatus.UNAUTHORIZED, response="Invalid token")

        try:
            user_dto = user_service.get_user_by_public_id(public_id=token["public_id"])
        except UserNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="User not found")

        return make_response(code=200, **user_dto.model_dump())
