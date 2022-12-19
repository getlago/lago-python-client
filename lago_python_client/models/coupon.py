from pydantic import BaseModel, Field
from typing import Optional


class Coupon(BaseModel):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    expiration: Optional[str]
    expiration_at: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    reusable: Optional[bool]
    frequency: Optional[str]
    frequency_duration: Optional[int]


class CouponResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    expiration: str
    expiration_at: Optional[str]
    percentage_rate: Optional[float]
    coupon_type: Optional[str]
    reusable: Optional[bool]
    frequency: Optional[str]
    frequency_duration: Optional[int]
