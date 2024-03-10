from schema_registry.models.v1.billing_cycle_closed_event import (
    BillingCycleClosedEventSchema,
)
from schema_registry.models.v1.billing_cycle_started_event import (
    BillingCycleStartedEventSchema,
)

from src.dto.billing import BillingCycleDTO
from src.kafka.producer import EventsProducer
from src.repositories.billing import BillingCycleRepository
from src.services.exceptions import BillingCycleNotFound


class BillingCycleService:
    def __init__(self, billing_repo: BillingCycleRepository, producer: EventsProducer):
        self.billing_repo = billing_repo
        self.producer = producer

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

        self.producer.send(
            value=closed_cycle_event_dto.model_dump_json(),
            topic="billings",
        )
        self.producer.send(
            value=started_cycle_event_dto.model_dump_json(),
            topic="billings",
        )
