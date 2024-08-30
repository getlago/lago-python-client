from typing import List, Optional

from ..base_model import BaseResponseModel


class GrossRevenueResponse(BaseResponseModel):
    amount_cents: Optional[int]
    currency: Optional[str]
    month: str
    invoices_count: int


class GrossRevenuesResponse(BaseResponseModel):
    __root__: List[GrossRevenueResponse]
