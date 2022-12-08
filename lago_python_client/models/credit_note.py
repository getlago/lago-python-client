from pydantic import BaseModel
from typing import Optional, List
from .invoice import FeeResponse

class ItemResponse(BaseModel):
    lago_id: Optional[str]
    credit_amount_cents: Optional[int]
    credit_amount_currency: Optional[str]
    refund_amount_cents: Optional[int]
    refund_amount_currency: Optional[str]
    fee: Optional[FeeResponse]

class ItemsResponse(BaseModel):
    __root__: List[ItemResponse]

class CreditNoteResponse(BaseModel):
    lago_id: Optional[str]
    sequential_id: Optional[int]
    number: Optional[str]
    lago_invoice_id: Optional[str]
    invoice_number: Optional[str]
    credit_status: Optional[str]
    refund_status: Optional[str]
    reason: Optional[str]
    total_amount_cents: Optional[int]
    total_amount_currency: Optional[str]
    credit_amount_cents: Optional[int]
    credit_amount_currency: Optional[str]
    balance_amount_cents: Optional[int]
    balance_amount_currency: Optional[str]
    refund_amount_cents: Optional[int]
    refund_amount_currency: Optional[str]
    vat_amount_cents: Optional[str]
    vat_amount_currency: Optional[str]
    sub_total_vat_excluded_amount_cents: Optional[str]
    sub_total_vat_excluded_amount_currency: Optional[str]
    file_url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    items: Optional[ItemsResponse]

class Item(BaseModel):
    credit_amount_cents: Optional[int]
    refund_amount_cents: Optional[int]
    fee_id: Optional[str]

class Items(BaseModel):
    __root__: List[Item]

class CreditNote(BaseModel):
    reason: Optional[str]
    items: Optional[Items]

class CreditNoteUpdate(BaseModel):
    refund_status: Optional[str]
