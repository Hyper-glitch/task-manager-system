from src.database import db
from src.models.base import Base
from src.models.billing_cycle import BillingCycle
from src.models.user import User


class Account(Base):
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Ineger, default=0)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey(User.id))
    billing_cycle_id = db.Column(
        "billing_cycle_id", db.Integer, db.ForeignKey(BillingCycle.id)
    )
