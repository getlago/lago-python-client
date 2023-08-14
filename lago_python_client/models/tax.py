from typing import List, Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class Tax(BaseModel):
    name: Optional[str]
    code: Optional[str]
    rate: Optional[float]
    description: Optional[str]
    applied_to_organization: Optional[bool]


class Taxes(BaseModel):
    __root__: List[Tax]


class TaxResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    rate: float
    description: Optional[str]
    add_ons_count: int
    customers_count: int
    plans_count: int
    charges_count: int
    applied_to_organization: bool
    created_at: str


class TaxesResponse(BaseResponseModel):
    __root__: List[TaxResponse]
