from typing import Any, List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class LimitationConfiguration(BaseModel):
    plan_codes: Optional[List[Any]]
    billable_metric_codes: Optional[List[Any]]


class Coupon(BaseModel):
    name: Optional[str]
    code: Optional[str]
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    expiration: Optional[str]
    expiration_at: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    reusable: Optional[bool]
    frequency: Optional[str]
    frequency_duration: Optional[int]
    applies_to: Optional[LimitationConfiguration]


class CouponResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    created_at: str
    expiration: str
    expiration_at: Optional[str]
    terminated_at: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    reusable: Optional[bool]
    frequency: Optional[str]
    frequency_duration: Optional[int]
    plan_codes: Optional[List[Any]]
    limited_plans: Optional[bool]
    billable_metric_codes: Optional[List[Any]]
    limited_billable_metrics: Optional[bool]
