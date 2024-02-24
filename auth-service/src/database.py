from flask_sqlalchemy import SQLAlchemy

from src.models.base import Base

db = SQLAlchemy(model_class=Base)
