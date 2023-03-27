from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class AppliedAddOn(BaseModel):
    external_customer_id: str
    add_on_code: str
    amount_cents: Optional[int]
    amount_currency: Optional[str]


class AppliedAddOnResponse(BaseResponseModel):
    lago_id: str
    lago_add_on_id: str
    add_on_code: str
    external_customer_id: str
    lago_customer_id: str
    amount_cents: int
    amount_currency: str
    created_at: str
