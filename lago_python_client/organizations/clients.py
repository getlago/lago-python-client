from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import UpdateCommandMixin
from ..models.organization import OrganizationResponse


class OrganizationClient(UpdateCommandMixin[OrganizationResponse], BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[OrganizationResponse]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'
