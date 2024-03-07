from http import HTTPStatus

from flask import Response
from flask_restx import Resource, reqparse

from src.services import billing_service, acc_service
from src.services.exceptions import BillingCycleNotFound
from src.utils import make_response


class BillingCycle(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('billing_cycle_id', type=int)
    parser.add_argument('limit', type=int)
    parser.add_argument('offset', type=int)
    parser.add_argument('user_id', type=int)

    def get(self) -> Response:
        data = self.parser.parse_args()
        try:
            billing_cycle = billing_service.get_billing_cycle(billing_cycle_id=data["billing_cycle_id"])
        except BillingCycleNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="Billing cycle not found")
        else:
            return make_response(code=200, **billing_cycle.model_dump())

    def get_balances(self) -> Response:
        data = self.parser.parse_args()
        count = acc_service.get_balances(
            billing_cycle_id=data["billing_cycle_id"],
            user_id=data["user_id"],
            limit=data["limit"],
            offset=data["offset"],
        )
        balance = acc_service.get_acc_balance(
            billing_cycle_id=data["billing_cycle_id"],
            user_id=data["user_id"],
        )
        return make_response(code=200, **{"balance": balance, "pagination_count": count})
