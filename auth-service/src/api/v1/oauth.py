from http import HTTPStatus

from flask import Response, redirect
from flask_restx import Resource, reqparse

from src.services import user_service, oauth_service
from src.services.exceptions import UserNotFound


class OAuth(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('response_type', type=str)
    parser.add_argument('redirect_uri', type=str)
    parser.add_argument('beak_shape', type=str)

    def get(self) -> Response:
        data = OAuth.parser.parse_args()

        if data["response_type"] != "code":
            return Response(
                status=HTTPStatus.BAD_REQUEST,
                response="Invalid response type",
            )

        try:
            user = user_service.identify_user_by_beak_shape(beak_shape=data["beak_shape"])
        except UserNotFound:
            return Response(status=HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, response=str(exc))
        else:
            auth_code = oauth_service.generate_auth_code(user)
            return redirect(location=f"{data['redirect_uri']}?code={auth_code}")
