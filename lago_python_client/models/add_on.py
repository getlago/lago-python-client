from pydantic import BaseModel, Field
from typing import Optional


class AddOn(BaseModel):
    name: Optional[str]
    code: Optional[str]
    amount_cents: Optional[int]
    amount_currency: Optional[str]
    description: Optional[str]


class AddOnResponse(BaseModel):
    lago_id: str
    name: str
    code: str
    amount_cents: int
    amount_currency: str
    created_at: str
    description: Optional[str]
