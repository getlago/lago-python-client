from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class Payment(BaseModel):
    invoice_id: str
    amount_cents: int
    reference: str
    paid_at: Optional[str]


class PaymentResponse(BaseResponseModel):
    lago_id: str
    invoice_ids: List[str]
    amount_cents: int
    amount_currency: str
    payment_status: str
    type: str
    reference: str
    external_payment_id: Optional[str]
    created_at: str


class PaymentsResponse(BaseResponseModel):
    __root__: List[PaymentResponse]
