from pydantic import BaseModel, Field
from typing import Optional


class Event(BaseModel):
    transaction_id: str
    customer_id: str
    code: str
    timestamp: Optional[int]
    properties: Optional[dict]
