from pydantic import BaseModel, Field
from typing import Optional


class Event(BaseModel):
    transaction_id: str
    customer_id: str
    code: str
    timestamp: Optional[int]
    properties: Optional[dict]

class EventResponse(BaseModel):
    lago_id: str
    transaction_id: str
    customer_id: str
    code: str
    timestamp: str
    properties: Optional[dict]
    created_at: str
