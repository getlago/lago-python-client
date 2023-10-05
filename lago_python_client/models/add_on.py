from typing import List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel

from .tax import TaxesResponse

class AddOn(BaseModel):
    name: Optional[str]
    invoice_display_name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    description: Optional[str]
    tax_codes: Optional[List[str]]


class AddOnResponse(BaseResponseModel):
    lago_id: str
    name: str
    invoice_display_name: Optional[str]
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    description: Optional[str]
    taxes: Optional[TaxesResponse]
