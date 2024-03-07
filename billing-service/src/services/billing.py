from src.dto.billing import BillingCycleDTO
from src.repositories.billing import BillingCycleRepository
from src.services.exceptions import BillingCycleNotFound


class BillingCycleService:
    def __init__(self, billing_repo: BillingCycleRepository, broker):
        self.billing_repo = billing_repo
        self.broker = broker

    def get_billing_cycle(self, billing_cycle_id: int) -> BillingCycleDTO:
        billing = self.billing_repo.get_by_id(billing_cycle_id=billing_cycle_id)
        if not billing:
            raise BillingCycleNotFound(f"Billing {billing_cycle_id} not found")

        billing_dto = BillingCycleDTO.from_orm(billing)
        return billing_dto

    def close_cycle(self) -> None:
        cycle = self.billing_repo.get_last(lock=True)
        closed_cycle = self.billing_repo.close(cycle=cycle)
        active_cycle = self.billing_repo.create_active()

        closed_cycle_event_dto = BillingCycleClosedEventSchema.from_orm(closed_cycle)
        started_cycle_event_dto = BillingCycleStartedEventSchema.from_orm(active_cycle)

        self.broker.send(closed_cycle_event_dto, f"{closed_cycle_event_dto.title}.{closed_cycle_event_dto.version}")
        self.broker.send(started_cycle_event_dto, f"{started_cycle_event_dto.title}.{started_cycle_event_dto.version}")
