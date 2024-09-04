from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, FindAllCommandMixin
from ..models.payment_request import PaymentRequestResponse


class PaymentRequestClient(
    CreateCommandMixin[PaymentRequestResponse],
    FindAllCommandMixin[PaymentRequestResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "payment_requests"
    RESPONSE_MODEL: ClassVar[Type[PaymentRequestResponse]] = PaymentRequestResponse
    ROOT_NAME: ClassVar[str] = "payment_request"
