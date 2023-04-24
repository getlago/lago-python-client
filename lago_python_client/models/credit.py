from typing import List, Optional

from pydantic import BaseModel

from .invoice_item import InvoiceItemResponse
from ..base_model import BaseResponseModel


class InvoiceShortDetails(BaseModel):
    lago_id: Optional[str]
    payment_status: Optional[str]


class CreditResponse(BaseResponseModel):
    lago_id: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    before_vat: bool
    item: Optional[InvoiceItemResponse]
    invoice: Optional[InvoiceShortDetails]


class CreditsResponse(BaseResponseModel):
    __root__: List[CreditResponse]
