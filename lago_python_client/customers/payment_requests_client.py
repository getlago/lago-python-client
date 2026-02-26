from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.payment_request import PaymentRequestResponse
from .clients import CustomerClient


class CustomerPaymentRequestsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "payment_requests"
    RESPONSE_MODEL: ClassVar[Type[PaymentRequestResponse]] = PaymentRequestResponse
    ROOT_NAME: ClassVar[str] = "payment_request"
