from pydantic import BaseModel, Field
from typing import Optional


class InvoicePaymentStatusChange(BaseModel):
    payment_status: str


class InvoiceResponse(BaseModel):
    lago_id: str
    sequential_id: int
    issuing_date: Optional[str]
    invoice_type: str
    payment_status: str
    amount_cents: int
    amount_currency: str
    vat_amount_cents: int
    vat_amount_currency: str
    total_amount_cents: int
    total_amount_currency: str
    file_url: Optional[str]
