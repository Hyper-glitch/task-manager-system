from http import HTTPStatus

from flask import Response
from flask_restx import Resource, reqparse

from src.services import task_service
from src.services.exceptions import TaskNotFound
from src.utils import make_response


class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('task_id', type=str)

    def get(self) -> Response:
        data = Task.parser.parse_args()
        try:
            task_dto = task_service.get_task(task_id=data["task_id"])
        except TaskNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="Task not found")
        return make_response(code=200, **task_dto.model_dump())

    def post(self) -> Response:
        data = Task.parser.parse_args()
        try:
            task_dto = task_service.add_task(data=data)
        except TaskNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="Task not found")
        return make_response(code=200, **task_dto.model_dump())


class TaskComplete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('task_id', type=str)

    def post(self) -> Response:
        data = Task.parser.parse_args()
        try:
            task_dto = task_service.complete_task(task_id=data["task_id"])
        except TaskNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="Task not found")
        return make_response(code=200, **task_dto.model_dump())
