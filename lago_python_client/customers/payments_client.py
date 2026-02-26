from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.payment import PaymentResponse
from .clients import CustomerClient


class CustomerPaymentsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "payments"
    RESPONSE_MODEL: ClassVar[Type[PaymentResponse]] = PaymentResponse
    ROOT_NAME: ClassVar[str] = "payment"
