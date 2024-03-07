from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy import desc

from src.enums.billing_cycle import BillingCycleStatus
from src.models.billing_cycle import BillingCycle
from src.services.exceptions import NoActiveCycleError


class BillingCycleRepository:
    def __init__(
            self,
            session: Session,
    ):
        self._session = session

    def get_by_id(self, billing_cycle_id: int) -> BillingCycle | None:
        return self._session.query(BillingCycle).filter(BillingCycle.id == billing_cycle_id).first()

    def get_last(
        self, lock: bool = False, **lock_params: Any
    ) -> BillingCycle | None:
        query = self._session.query(BillingCycle)
        if lock:
            query = query.with_for_update(**lock_params)

        cycle = query.order_by(desc(BillingCycle.id)).first()
        if cycle and cycle.status != BillingCycleStatus.ACTIVE:
            raise NoActiveCycleError
        return cycle

    def get_last_closed(
        self, lock: bool = False, **lock_params: Any
    ) -> BillingCycle | None:
        query = self._session.query(BillingCycle)
        if lock:
            query = query.with_for_update(**lock_params)

        cycles = query.filter(
            BillingCycle.status == BillingCycleStatus.CLOSED
        ).all()
        if cycles:
            return cycles[0]

    def close(self, cycle: BillingCycle) -> BillingCycle:
        cycle.status = BillingCycleStatus.CLOSED
        cycle.closed_at = datetime.utcnow()
        self._session.commit()
        return cycle

    def create_active(self) -> BillingCycle:
        cycle = BillingCycle()
        self._session.add(cycle)
        self._session.commit()
        return cycle

    def get_cycle_with_satus(self, status: BillingCycleStatus) -> BillingCycle | None:
        cycle = BillingCycle()
        cycle.status = status
        cycle.processed_at = datetime.utcnow()
        self._session.commit()
        return cycle

    def get_list(
        self,
        limit: int,
        offset: int,
    ) -> list[BillingCycle]:
        return self._session.query(BillingCycle).order_by(desc(BillingCycle.id)).offset(offset).limit(limit).all()

    def count_all(self) -> int:
        return self._session.query(BillingCycle).count()
