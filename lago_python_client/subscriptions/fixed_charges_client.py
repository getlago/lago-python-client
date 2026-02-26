from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    FindAllChildrenCommandMixin,
    FindChildCommandMixin,
    UpdateChildCommandMixin,
)
from ..models.fixed_charge import FixedChargeResponse


class SubscriptionFixedChargesClient(
    FindAllChildrenCommandMixin[FixedChargeResponse],
    FindChildCommandMixin[FixedChargeResponse],
    UpdateChildCommandMixin[FixedChargeResponse],
    BaseClient,
):
    PARENT_API_RESOURCE: ClassVar[str] = "subscriptions"
    API_RESOURCE: ClassVar[str] = "fixed_charges"
    RESPONSE_MODEL: ClassVar[Type[FixedChargeResponse]] = FixedChargeResponse
    ROOT_NAME: ClassVar[str] = "fixed_charge"
