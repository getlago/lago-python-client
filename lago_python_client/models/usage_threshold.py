from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class UsageThreshold(BaseModel):
    id: Optional[str]
    threshold_display_name: Optional[str]
    amount_cents: int
    recurring: bool


class UsageThresholds(BaseModel):
    __root__: List[UsageThreshold]


class UsageThresholdResponse(BaseResponseModel):
    lago_id: str
    threshold_display_name: Optional[str]
    amount_cents: int
    recurring: bool
    created_at: str
    updated_at: str


class UsageThresholdsResponse(BaseResponseModel):
    __root__: List[UsageThresholdResponse]


class AppliedUsageThresholdResponse(BaseResponseModel):
    lifetime_usage_amount_cents: int
    created_at: str
    usage_threshold: UsageThresholdResponse


class AppliedUsageThresholdsResponse(BaseResponseModel):
    __root__: List[AppliedUsageThresholdResponse]
