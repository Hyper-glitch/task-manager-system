from src.dto.billing import BillingCycleDTO
from src.repositories.billing import BillingCycleRepository
from src.services.exceptions import BillingCycleNotFound


class BillingCycleService:
    def __init__(self, billing_repo: BillingCycleRepository):
        self.billing_repo = billing_repo

    def get_billing_cycle(self, billing_cycle_id: int) -> BillingCycleDTO:
        billing = self.billing_repo.get_by_id(billing_cycle_id=billing_cycle_id)
        if not billing:
            raise BillingCycleNotFound(f"Billing {billing_cycle_id} not found")

        billing_dto = BillingCycleDTO.from_orm(billing)
        return billing_dto
