from flask import Blueprint
from flask_restx import Api

from src.api.v1 import balance, task_cost

balance_blueprint = Blueprint("balance", __name__, url_prefix="/balance")
balance_api = Api(balance_blueprint)
balance_api.add_namespace(balance.namespace)


blueprint = Blueprint("task_cost", __name__, url_prefix="/task_cost")
task_cost_api = Api(blueprint)
task_cost_api.add_namespace(task_cost.namespace)
