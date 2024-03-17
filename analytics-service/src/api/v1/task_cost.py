from flask import Response
from flask_restx import Resource, Namespace, reqparse

from src.services import task_cost_service
from src.utils import make_response

namespace = Namespace("task_cost")


class TaskCost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('period', type=str)

    @namespace.route("/most_expensive_task")
    def get_most_expensive_task(self) -> Response:
        data = self.parser.parse_args()
        task = task_cost_service.get_most_expensive_task(period=data["task"])
        return make_response(code=200, **task)
