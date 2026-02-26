from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateChildCommandMixin,
    DestroyChildCommandMixin,
    FindAllChildrenCommandMixin,
    FindChildCommandMixin,
    UpdateChildCommandMixin,
)
from ..models.charge import ChargeResponse


class PlanChargesClient(
    FindAllChildrenCommandMixin[ChargeResponse],
    FindChildCommandMixin[ChargeResponse],
    CreateChildCommandMixin[ChargeResponse],
    UpdateChildCommandMixin[ChargeResponse],
    DestroyChildCommandMixin[ChargeResponse],
    BaseClient,
):
    PARENT_API_RESOURCE: ClassVar[str] = "plans"
    API_RESOURCE: ClassVar[str] = "charges"
    RESPONSE_MODEL: ClassVar[Type[ChargeResponse]] = ChargeResponse
    ROOT_NAME: ClassVar[str] = "charge"
