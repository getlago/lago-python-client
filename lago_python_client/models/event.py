from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Event(BaseModel):
    transaction_id: str
    external_customer_id: Optional[str]
    external_subscription_id: Optional[str]
    code: str
    timestamp: Optional[int]
    properties: Optional[Dict[str, Any]]


class BatchEvent(BaseModel):
    transaction_id: str
    external_customer_id: Optional[str]
    external_subscription_ids: List[str]
    code: str
    timestamp: Optional[int]
    properties: Optional[Dict[str, Any]]


class EventResponse(BaseModel):
    lago_id: str
    transaction_id: str
    external_customer_id: Optional[str]
    lago_customer_id: Optional[str]
    lago_subscription_id: Optional[str]
    external_subscription_id: Optional[str]
    code: str
    timestamp: str
    properties: Optional[Dict[str, Any]]
    created_at: str
