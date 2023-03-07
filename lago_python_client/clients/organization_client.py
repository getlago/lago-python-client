from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.organization import OrganizationResponse


class OrganizationClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'

    def prepare_response(self, data: Dict[Any, Any]) -> BaseModel:
        return self.RESPONSE_MODEL.parse_obj(data)
