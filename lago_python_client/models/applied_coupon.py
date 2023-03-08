from pydantic import BaseModel, Field
from typing import Optional
from .credit import CreditsResponse


class AppliedCoupon(BaseModel):
    external_customer_id: str
    coupon_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    percentage_rate: Optional[float]
    frequency: Optional[str]
    frequency_duration: Optional[int]


class AppliedCouponResponse(BaseModel):
    lago_id: str
    lago_coupon_id: str
    coupon_code: str
    status: Optional[str]
    external_customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_cents_remaining: Optional[int]
    amount_currency: str
    expiration_date: Optional[str]
    created_at: str
    terminated_at: Optional[str]
    percentage_rate: Optional[float]
    frequency: Optional[str]
    frequency_duration: Optional[int]
    frequency_duration_remaining: Optional[int]
    credits: Optional[CreditsResponse]
