from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin
from ..models.applied_add_on import AppliedAddOnResponse


class AppliedAddOnClient(
    CreateCommandMixin[AppliedAddOnResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    RESPONSE_MODEL: ClassVar[Type[AppliedAddOnResponse]] = AppliedAddOnResponse
    ROOT_NAME: ClassVar[str] = 'applied_add_on'
