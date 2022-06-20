from pydantic import BaseModel, Field
from typing import Optional


class InvoiceStatusChange(BaseModel):
    lago_id: str
    status: str


class InvoiceResponse(BaseModel):
    lago_id: str
    sequential_id: int
    from_date: Optional[str]
    to_date: Optional[str]
    charges_from_date: Optional[str]
    issuing_date: Optional[str]
    invoice_type: str
    status: str
    amount_cents: int
    amount_currency: str
    vat_amount_cents: int
    vat_amount_currency: str
    total_amount_cents: int
    total_amount_currency: str
