from typing import List, Optional

from lago_python_client.base_model import BaseModel

from ..base_model import BaseResponseModel


class WebhookEndpoint(BaseModel):
    webhook_url: Optional[str]
    signature_algo: Optional[str]
    name: Optional[str]
    event_types: Optional[List[str]]


class WebhookEndpointResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    webhook_url: str
    signature_algo: Optional[str]
    name: Optional[str]
    event_types: Optional[List[str]]
    created_at: str
