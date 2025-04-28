from typing import List

from ..base_model import BaseResponseModel
from .payment import PaymentResponse


class PaymentReceiptResponse(BaseResponseModel):
    lago_id: str
    number: str
    payment: PaymentResponse
    created_at: str


class PaymentReceiptsResponse(BaseResponseModel):
    __root__: List[PaymentReceiptResponse]
