from datetime import datetime, date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.models.task_cost import TaskCost


class TaskCostService:
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def get_most_expensive_task(self, period: str):
        end_day = datetime.today()
        start_day = None

        if period == "1d":
            end_day = datetime.combine(date.today(), datetime.max.time())
            start_day = datetime.combine(date.today(), datetime.min.time())
        elif period == "7d":
            start_day = end_day - timedelta(days=7)
        elif period == "1m":
            start_day = end_day - timedelta(days=30)

        expensive_task = (
            self._session.query(TaskCost)
            .filter(func.max(TaskCost.debit))
            .filter(TaskCost.created_at.between(start_day, end_day))
            .first()
        )
        return {
            "most_expensive_task": expensive_task
        }
