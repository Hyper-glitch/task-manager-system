from http import HTTPStatus

from flask import Response, redirect
from flask_restx import Resource, reqparse

from src.constants import ROLES_SCOPE_MAP
from src.enums.grant_type import GrantType
from src.services import oauth_service
from src.services.exceptions import UserNotFound, AuthorizationCodeInvalid, InvalidTokenException
from src.utils import make_response


class OAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('response_type', type=str)
    parser.add_argument('redirect_uri', type=str)
    parser.add_argument('beak_shape', type=str)
    parser.add_argument('grant_type', type=str)
    parser.add_argument('code', type=str)
    parser.add_argument('refresh_token', type=str)

    def get(self) -> Response:
        data = OAuth.parser.parse_args()

        if data["response_type"] != "code":
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                response="Invalid response type",
            )

        try:
            user = oauth_service.identify_user_by_beak_shape(beak_shape=data["beak_shape"])
        except UserNotFound:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=str(exc))
        else:
            auth_code = oauth_service.generate_auth_code(user)
            return redirect(location=f"{data['redirect_uri']}?code={auth_code}")

    def post(self) -> Response:
        data = OAuth.parser.parse_args()

        if data["grant_type"] == GrantType.AUTHORIZATION_CODE.value:
            if data["code"] is None:
                return Response(
                    status=HTTPStatus.BAD_REQUEST,
                    response="Missing authorization code",
                )
            try:
                user = oauth_service.identify_user_by_auth_code(code=data["code"])
            except (AuthorizationCodeInvalid, UserNotFound):
                return Response(status=HTTPStatus.UNAUTHORIZED)

        elif data["grant_type"] == GrantType.REFRESH_TOKEN.value:
            if data["refresh_token"] is None:
                return Response(
                    status=HTTPStatus.BAD_REQUEST,
                    response="Missing refresh token",
                )
            try:
                user = oauth_service.identify_user_by_refresh_token(refresh_token=data["refresh_token"])
            except (UserNotFound, InvalidTokenException):
                return Response(status=HTTPStatus.UNAUTHORIZED)

        else:
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                response="Invalid grant type",
            )

        token_pair = oauth_service.create_token(user)
        data = {
                "access_token": token_pair.access_token,
                "refresh_token": token_pair.refresh_token,
                "scopes": ROLES_SCOPE_MAP.get(user.role, []),
                "info": {
                    "id": user.id,
                    "public_id": user.public_id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                },
            }
        return make_response(code=200, **data)
