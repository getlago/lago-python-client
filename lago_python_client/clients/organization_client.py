from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from ..models.organization import OrganizationResponse


class OrganizationClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'
