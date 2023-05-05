from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class TaxRate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    value: Optional[float]
    description: Optional[str]


class TaxRateResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    value: float
    description: Optional[str]
    customers_count: int
    created_at: str
