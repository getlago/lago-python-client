from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class TaxRate(BaseModel):
    name: Optional[str]
    code: Optional[str]
    value: Optional[float]
    description: Optional[str]
    applied_by_default: Optional[bool]


class TaxRateResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    value: float
    description: Optional[str]
    customers_count: int
    applied_by_default: bool
    created_at: str
