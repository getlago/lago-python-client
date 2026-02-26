from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel
from .invoice_item import InvoiceItemResponse


class InvoiceShortDetails(BaseModel):
    lago_id: Optional[str]
    payment_status: Optional[str]


class CreditResponse(BaseResponseModel):
    lago_id: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    before_taxes: bool
    item: Optional[InvoiceItemResponse]
    invoice: Optional[InvoiceShortDetails]


class CreditsResponse(BaseResponseModel):
    __root__: List[CreditResponse]
