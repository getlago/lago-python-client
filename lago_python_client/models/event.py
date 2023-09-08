from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class Event(BaseModel):
    transaction_id: str
    external_customer_id: Optional[str]
    external_subscription_id: Optional[str]
    code: str
    timestamp: Optional[Union[int, str]]
    properties: Optional[Dict[str, Any]]


class BatchEvent(BaseModel):
    transaction_id: str
    external_customer_id: Optional[str]
    external_subscription_ids: List[str]
    code: str
    timestamp: Optional[Union[int, str]]
    properties: Optional[Dict[str, Any]]


class EventResponse(BaseResponseModel):
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
