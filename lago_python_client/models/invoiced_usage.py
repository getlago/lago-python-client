from typing import List, Optional

from ..base_model import BaseModel, BaseResponseModel


class InvoicedUsageResponse(BaseResponseModel):
    amount_cents: int
    code: Optional[str]
    currency: str
    month: str


class InvoicedUsagesResponse(BaseResponseModel):
    __root__: List[InvoicedUsageResponse]
