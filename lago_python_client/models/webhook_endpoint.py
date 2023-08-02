from typing import Optional

from pydantic import BaseModel

from ..base_model import BaseResponseModel


class WebhookEndpoint(BaseModel):
    webhook_url: Optional[str]


class WebhookEndpointResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    webhook_url: str
    signature_algo: Optional[str]
    created_at: str
