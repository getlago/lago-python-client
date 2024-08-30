from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class UsageThreshold(BaseModel):
    id: Optional[str]
    threshold_display_name: Optional[str]
    amount_cents: Optional[int]
    recurring: Optional[bool]


class UsageThresholds(BaseModel):
    __root__: List[UsageThreshold]


class UsageThresholdResponse(BaseResponseModel):
    lago_id: str
    amount_cents: int
    threshold_display_name: Optional[str]
    recurring: bool
    created_at: Optional[str]
    updated_at: Optional[str]


class UsageThresholdsResponse(BaseResponseModel):
    __root__: List[UsageThresholdResponse]


class UsageThresholdOverrides(BaseModel):
    amount_cents: Optional[int]
    threshold_display_name: Optional[str]
    recurring: Optional[bool]


class UsageThresholdsOverrides(BaseModel):
    __root__: List[UsageThresholdOverrides]
