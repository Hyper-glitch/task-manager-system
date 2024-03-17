from flask import Response
from flask_restx import Resource, Namespace

from src.services import balance_service
from src.utils import make_response

namespace = Namespace("balance")


class Balance(Resource):
    @namespace.route("/managers/today")
    def get_managers_balances(self) -> Response:
        managers_income = balance_service.get_today_manager_balance()
        return make_response(code=200, **managers_income)

    @namespace.route("/workers/today")
    def get_workers_balances(self) -> Response:
        worker_balances = balance_service.get_worker_statuses()
        return make_response(code=200, **worker_balances)
