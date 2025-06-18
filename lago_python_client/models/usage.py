from typing import List

from ..base_model import BaseResponseModel


class UsageResponse(BaseResponseModel):
    organization_id: str
    start_of_period_dt: str
    end_of_period_dt: str
    amount_currency: str
    amount_cents: int
    billable_metric_code: str
    units: float
    is_billable_metric_deleted: bool


class UsagesResponse(BaseResponseModel):
    __root__: List[UsageResponse]
