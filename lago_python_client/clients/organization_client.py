from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.organization import OrganizationResponse


class OrganizationClient(
    CreateCommandMixin[OrganizationResponse],
    DestroyCommandMixin[OrganizationResponse],
    FindAllCommandMixin[OrganizationResponse],
    FindCommandMixin[OrganizationResponse],
    UpdateCommandMixin[OrganizationResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'organizations'
    RESPONSE_MODEL: ClassVar[Type[OrganizationResponse]] = OrganizationResponse
    ROOT_NAME: ClassVar[str] = 'organization'
