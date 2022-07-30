from pydantic import BaseModel, Field
from typing import Optional, List


class Event(BaseModel):
    transaction_id: str
    customer_id: Optional[str]
    subscription_id: Optional[str]
    code: str
    timestamp: Optional[int]
    properties: Optional[dict]


class BatchEvent(BaseModel):
    transaction_id: str
    customer_id: Optional[str]
    subscription_ids: List[str]
    code: str
    timestamp: Optional[int]
    properties: Optional[dict]


class EventResponse(BaseModel):
    lago_id: str
    transaction_id: str
    customer_id: Optional[str]
    lago_customer_id: Optional[str]
    lago_subscription_id: Optional[str]
    subscription_unique_id: Optional[str]
    code: str
    timestamp: str
    properties: Optional[dict]
    created_at: str
