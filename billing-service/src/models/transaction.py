import uuid
from datetime import datetime

from sqlalchemy import Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.database import db
from src.enums.transaction import TransactionTypes
from src.models.base import Base
from src.models.billing_cycle import BillingCycle


class Transaction(Base):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey(User.id))
    billing_cycle_id = db.Column(
        "billing_cycle_id", db.Integer, db.ForeignKey(BillingCycle.id)
    )
    debit = db.Column(
        "debit", db.Integer, nullable=False, default=0, server_default=db.text("0")
    )
    credit = db.Column(
        "credit", db.Integer, nullable=False, default=0, server_default=db.text("0")
    )
    task_id = db.Column("task_id", db.Integer)
    type = db.Column(
        "type",
        Enum(TransactionTypes),
        nullable=False,
        default=TransactionTypes.INCOME,
        server_default=db.text(f"'{TransactionTypes.INCOME.value}'"),
    )
    created_at = db.Column(
        "created_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=db.text("(now() at time zone 'utc')"),
    )
    task = db.relationship("Task", foreign_keys=[task_id])
    user = db.relationship("User", foreign_keys=[user_id])
    billing_cycle = db.relationship("BillingCycle", foreign_keys=[billing_cycle_id])
