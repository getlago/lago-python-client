from pydantic import BaseModel, Field
from typing import Optional


class Coupon(BaseModel):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    expiration: Optional[str]
    expiration_duration: Optional[int]


class CouponResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    expiration: str
    expiration_duration: Optional[int]
