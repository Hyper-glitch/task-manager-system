from flask import Flask

from src.config import settings
from src.database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.database_dsn
db.init_app(app)
