from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.organization import OrganizationResponse


class OrganizationClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'

    @classmethod
    def prepare_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
