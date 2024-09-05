from typing import Optional, List

from ..base_model import BaseResponseModel


class LifetimeUsageThresholdResponse(BaseResponseModel):
    amount_cents: int
    completion_ratio: float
    reached_at: Optional[str]


class LifetimeUsageResponse(BaseResponseModel):
    lago_id: str
    lago_subscription_id: str
    external_subscription_id: str
    external_historical_usage_amount_cents: int
    invoiced_usage_amount_cents: int
    current_usage_amount_cents: int
    from_datetime: Optional[str]
    to_datetime: Optional[str]
    usage_thresholds: Optional[List[LifetimeUsageThresholdResponse]]
