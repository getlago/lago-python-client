from typing import List, Optional

from .invoice_item import InvoiceItemResponse
from ..base_model import BaseModel, BaseResponseModel

class Fee(BaseModel):
    payment_status: Optional[str]

class FeeResponse(BaseResponseModel):
    lago_id: Optional[str]
    lago_group_id: Optional[str]
    lago_invoice_id: Optional[str]
    lago_true_up_fee_id: Optional[str]
    lago_true_up_parent_fee_id: Optional[str]
    external_subscription_id: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    vat_amount_cents: Optional[int]
    vat_amount_currency: Optional[str]
    total_amount_cents: Optional[int]
    unit_amount_cents: Optional[int]
    total_amount_currency: Optional[str]
    units: Optional[float]
    events_count: Optional[int]
    payment_status: Optional[str]
    created_at: Optional[str]
    description: Optional[str]
    pay_in_advance: Optional[bool]
    invoiceable: Optional[bool]
    succeeded_at: Optional[str]
    failed_at: Optional[str]
    refunded_at: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]

    item: Optional[InvoiceItemResponse]


class FeesResponse(BaseResponseModel):
    __root__: List[FeeResponse]
