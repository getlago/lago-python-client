from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class OutstandingInvoiceResponse(BaseResponseModel):
    amount_cents: int
    currency: Optional[str]
    month: str
    invoices_count: int
    payment_status: Optional[str]


class OutstandingInvoicesResponse(BaseResponseModel):
    __root__: List[OutstandingInvoiceResponse]
