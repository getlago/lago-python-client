from typing import List, Optional

from pydantic import BaseModel

from .invoice_item import InvoiceItemResponse


class InvoiceShortDetails(BaseModel):
    lago_id: Optional[str]
    payment_status: Optional[str]


class CreditResponse(BaseModel):
    lago_id: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    item: Optional[InvoiceItemResponse]
    invoice: Optional[InvoiceShortDetails]


class CreditsResponse(BaseModel):
    __root__: List[CreditResponse]
