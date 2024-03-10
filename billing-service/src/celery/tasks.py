from src.celery.app import app
from src.database import db
from src.models.account import Account
from src.services import billing_service, payment_service


@app.task
def close_cycle() -> None:
    billing_service.close_cycle()


@app.task
def send_payment(user_id: int, billing_cycle_id: int) -> None:
    payment_service.send_payment(user_id=user_id, billing_cycle_id=billing_cycle_id)


@app.task
def refresh_balance() -> None:
    db.session.execute(f"REFRESH MATERIALIZED VIEW {Account.__tablename__}")  # type: ignore
