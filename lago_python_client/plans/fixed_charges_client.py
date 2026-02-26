from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateChildCommandMixin,
    DestroyChildCommandMixin,
    FindAllChildrenCommandMixin,
    FindChildCommandMixin,
    UpdateChildCommandMixin,
)
from ..models.fixed_charge import FixedChargeResponse


class PlanFixedChargesClient(
    FindAllChildrenCommandMixin[FixedChargeResponse],
    FindChildCommandMixin[FixedChargeResponse],
    CreateChildCommandMixin[FixedChargeResponse],
    UpdateChildCommandMixin[FixedChargeResponse],
    DestroyChildCommandMixin[FixedChargeResponse],
    BaseClient,
):
    PARENT_API_RESOURCE: ClassVar[str] = "plans"
    API_RESOURCE: ClassVar[str] = "fixed_charges"
    RESPONSE_MODEL: ClassVar[Type[FixedChargeResponse]] = FixedChargeResponse
    ROOT_NAME: ClassVar[str] = "fixed_charge"
