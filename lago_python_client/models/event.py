from typing import Any, Dict, List, Optional, Union

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class Event(BaseModel):
    transaction_id: str
    external_subscription_id: str
    code: str
    timestamp: Optional[Union[int, str]]
    precise_total_amount_cents: Optional[str]
    properties: Optional[Dict[str, Any]]


class BatchEvent(BaseModel):
    events: List[Event]


class EventResponse(BaseResponseModel):
    lago_id: str
    transaction_id: str
    lago_customer_id: Optional[str]
    lago_subscription_id: Optional[str]
    external_subscription_id: str
    code: str
    timestamp: str
    precise_total_amount_cents: Optional[str]
    properties: Optional[Dict[str, Any]]
    created_at: str


class BatchEventResponse(BaseResponseModel):
    events: List[EventResponse]
