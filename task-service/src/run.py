from flask_restx import Api

from src.api.v1.task import Task
from src.api.v1.users import User
from src.app import create_app
from src.config import settings
from src.database import db

app = create_app()


def add_resource():
    api = Api(app)
    api.add_resource(User, 'api/v1/user')
    api.add_resource(Task, 'api/v1/authorize')


@app.before_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    add_resource()
    app.run(host=settings.api_host, port=settings.api_port)
