import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum, DateTime
from src.database import db
from src.enums.billing_cycle import BillingCycleStatus
from src.models.base import Base


class BillingCycle(Base):
    __tablename__ = "billing_cycle"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    status = db.Column(
        Enum(BillingCycleStatus),
        nullable=False,
        default=BillingCycleStatus.ACTIVE,
        server_default=db.text(f"'{BillingCycleStatus.ACTIVE.value}'"),
    )
    started_at = db.Column(
        "started_at",
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=db.text("(now() at time zone 'utc')"),
    )
    closed_at = (db.Column("closed_at", DateTime),)
