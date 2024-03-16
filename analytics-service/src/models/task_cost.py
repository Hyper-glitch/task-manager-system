import uuid

from sqlalchemy.dialects.postgresql import UUID

from src.database import db
from src.models.base import Base


class TaskCost(Base):
    __tablename__ = "task_cost"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    task_id = db.Column(db.String(128))
    title = db.Column(
        db.String(128), nullable=False, default="", server_default=db.text("''")
    )
    description = db.Column(
        db.Text, nullable=False, default="", server_default=db.text("''")
    )
    credit_cost = db.Column("credit_cost", db.Integer, nullable=False)
    debit_cost = db.Column("debit_cost", db.Integer, nullable=False)
