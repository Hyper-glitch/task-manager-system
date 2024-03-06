from http import HTTPStatus

from flask import Response
from flask_restx import Resource, reqparse

from src.services import billing_service
from src.services.exceptions import BillingCycleNotFound
from src.utils import make_response


class BillingCycle(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('billing_cycle_id', type=str)

    def get(self) -> Response:
        data = self.parser.parse_args()
        try:
            billing_cycle = billing_service.get_billing_cycle(billing_cycle_id=data["billing_cycle_id"])
        except BillingCycleNotFound:
            return Response(status=HTTPStatus.NOT_FOUND, response="Billing cycle not found")
        else:
            return make_response(code=200, **billing_cycle.model_dump())
