from pydantic import BaseModel, Field
from typing import Optional


class AppliedCoupon(BaseModel):
    customer_id: str
    coupon_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]


class AppliedCouponResponse(BaseModel):
    lago_id: str
    lago_coupon_id: str
    coupon_code: str
    customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_currency: str
    expiration_date: Optional[str]
    created_at: str
    terminated_at: Optional[str]
