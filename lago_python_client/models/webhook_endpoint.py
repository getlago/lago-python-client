from typing import List, Optional, Union

from lago_python_client.base_model import BaseModel, Field

from ..base_model import BaseResponseModel

from ..unset_type import UNSET, _UnsetType


class WebhookEndpoint(BaseModel):
    webhook_url: Union[str, None, _UnsetType] = Field(default=UNSET)
    signature_algo: Union[str, None, _UnsetType] = Field(default=UNSET)
    name: Union[str, None, _UnsetType] = Field(default=UNSET)
    event_types: Union[List[str], None, _UnsetType] = Field(default=UNSET)

    class Config:
        arbitrary_types_allowed = True

    def to_create_payload(self) -> dict:
        """Convert model to payload dict (for create requests)"""
        return self._to_payload()

    def to_update_payload(self) -> dict:
        """Convert model to payload dict (for update requests)"""
        return self._to_payload()

    def _to_payload(self) -> dict:
        """Convert model to payload dict (excluding Unset values, but preserving None values)"""
        data = self.dict()
        return {k: v for k, v in data.items() if not isinstance(v, _UnsetType)}


class WebhookEndpointResponse(BaseResponseModel):
    lago_id: str
    lago_organization_id: str
    webhook_url: str
    signature_algo: Optional[str]
    name: Optional[str]
    event_types: Optional[List[str]]
    created_at: str
