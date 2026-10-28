from typing import Any, Dict, List, Optional

from ..base_model import BaseModel, BaseResponseModel


class Payment(BaseModel):
    invoice_id: str
    amount_cents: int
    reference: str
    paid_at: Optional[str]


class PaymentResponse(BaseResponseModel):
    lago_id: str
    lago_customer_id: Optional[str]
    external_customer_id: Optional[str]
    invoice_ids: List[str]
    invoice_numbers: List[str]
    lago_payable_id: Optional[str]
    payable_type: Optional[str]
    amount_cents: int
    amount_currency: str
    status: Optional[str]
    payment_status: str
    type: str
    reference: str
    payment_provider_code: Optional[str]
    payment_provider_type: Optional[str]
    external_payment_id: Optional[str]
    provider_payment_id: Optional[str]
    provider_customer_id: Optional[str]
    next_action: Optional[Dict[str, Any]]
    created_at: str


class PaymentsResponse(BaseResponseModel):
    __root__: List[PaymentResponse]
