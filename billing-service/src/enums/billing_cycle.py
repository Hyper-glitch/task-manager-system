from enum import Enum


class BillingCycleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
