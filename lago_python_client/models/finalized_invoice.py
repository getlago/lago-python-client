from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class FinalizedInvoiceResponse(BaseResponseModel):
    amount_cents: int
    currency: Optional[str]
    month: str
    invoices_count: int
    payment_status: Optional[str]


class FinalizedInvoicesResponse(BaseResponseModel):
    __root__: List[FinalizedInvoiceResponse]
