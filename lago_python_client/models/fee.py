from pydantic import BaseModel, Field
from typing import Optional, List
from .invoice_item import InvoiceItemResponse

class FeeResponse(BaseModel):
    lago_id: Optional[str]
    item: Optional[InvoiceItemResponse]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    vat_amount_cents: Optional[int]
    vat_amount_currency: Optional[str]
    units: Optional[float]
    events_count: Optional[int]

class FeesResponse(BaseModel):
    __root__: List[FeeResponse]
