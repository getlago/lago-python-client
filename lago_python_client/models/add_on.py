from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class AddOn(BaseModel):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    description: Optional[str]


class AddOnResponse(BaseResponseModel):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    description: Optional[str]
