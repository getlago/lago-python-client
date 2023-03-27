from typing import List, Optional

from .invoice_item import InvoiceItemResponse
from ..base_model import BaseResponseModel


class FeeResponse(BaseResponseModel):
    lago_id: Optional[str]
    item: Optional[InvoiceItemResponse]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    vat_amount_cents: Optional[int]
    vat_amount_currency: Optional[str]
    total_amount_cents: Optional[int]
    total_amount_currency: Optional[str]
    units: Optional[float]
    events_count: Optional[int]


class FeesResponse(BaseResponseModel):
    __root__: List[FeeResponse]
