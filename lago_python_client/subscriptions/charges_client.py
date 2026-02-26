from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    FindAllChildrenCommandMixin,
    FindChildCommandMixin,
    UpdateChildCommandMixin,
)
from ..models.charge import ChargeResponse


class SubscriptionChargesClient(
    FindAllChildrenCommandMixin[ChargeResponse],
    FindChildCommandMixin[ChargeResponse],
    UpdateChildCommandMixin[ChargeResponse],
    BaseClient,
):
    PARENT_API_RESOURCE: ClassVar[str] = "subscriptions"
    API_RESOURCE: ClassVar[str] = "charges"
    RESPONSE_MODEL: ClassVar[Type[ChargeResponse]] = ChargeResponse
    ROOT_NAME: ClassVar[str] = "charge"
