from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.billing_entity import (
    BillingEntityResponse,
)


class BillingEntityClient(
    CreateCommandMixin[BillingEntityResponse],
    FindAllCommandMixin[BillingEntityResponse],
    FindCommandMixin[BillingEntityResponse],
    UpdateCommandMixin[BillingEntityResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "billing_entities"
    RESPONSE_MODEL: ClassVar[Type[BillingEntityResponse]] = BillingEntityResponse
    ROOT_NAME: ClassVar[str] = "billing_entity"
