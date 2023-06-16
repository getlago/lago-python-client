from typing import List, Optional

from pydantic import BaseModel

from .fee import FeeResponse
from ..base_model import BaseResponseModel


class ItemResponse(BaseResponseModel):
    lago_id: Optional[str]
    credit_amount_cents: Optional[int]
    credit_amount_currency: Optional[str]
    refund_amount_cents: Optional[int]
    refund_amount_currency: Optional[str]
    fee: Optional[FeeResponse]


class ItemsResponse(BaseResponseModel):
    __root__: List[ItemResponse]


class CreditNoteAppliedTax(BaseResponseModel):
    lago_id: Optional[str]
    lago_credit_note_id: Optional[str]
    lago_tax_id: Optional[str]
    tax_name: Optional[str]
    tax_code: Optional[str]
    tax_rate: Optional[float]
    tax_description: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    base_amount_cents: Optional[int]
    created_at: Optional[str]


class CreditNoteAppliedTaxes(BaseResponseModel):
    __root__: List[CreditNoteAppliedTax]


class CreditNoteResponse(BaseResponseModel):
    lago_id: Optional[str]
    sequential_id: Optional[int]
    number: Optional[str]
    lago_invoice_id: Optional[str]
    invoice_number: Optional[str]
    credit_status: Optional[str]
    refund_status: Optional[str]
    reason: Optional[str]
    currency: str
    total_amount_cents: int
    credit_amount_cents: int
    balance_amount_cents: int
    refund_amount_cents: int
    taxes_amount_cents: str
    taxes_rate: float
    sub_total_excluding_taxes_amount_cents: int
    coupons_adjustement_amount_cents: int
    file_url: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    items: Optional[ItemsResponse]
    applied_taxes: Optional[CreditNoteAppliedTaxes]


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
