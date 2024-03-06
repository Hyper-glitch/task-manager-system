from datetime import datetime

from pydantic import BaseModel

from src.enums.billing_cycle import BillingCycleStatus


class BillingCycleDTO(BaseModel):
    id: int
    public_id: str
    status: BillingCycleStatus
    started_at: datetime
    processed_at: datetime | None = None
    closed_at: datetime | None = None
