from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.organization import OrganizationResponse


class OrganizationClient(CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'
