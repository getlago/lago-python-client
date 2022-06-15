from pydantic import BaseModel, Field
from typing import Optional


class AppliedAddOn(BaseModel):
    customer_id: str
    add_on_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]


class AppliedAddOnResponse(BaseModel):
    lago_id: str
    lago_add_on_id: str
    add_on_code: str
    customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_currency: str
    created_at: str
