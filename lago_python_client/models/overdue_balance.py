from typing import List

from ..base_model import BaseResponseModel


class OverdueBalanceResponse(BaseResponseModel):
    amount_cents: int
    currency: str
    month: str
    lago_invoice_ids: List[str]


class OverdueBalancesResponse(BaseResponseModel):
    __root__: List[OverdueBalanceResponse]
