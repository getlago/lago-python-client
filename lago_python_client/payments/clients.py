from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, FindAllCommandMixin, FindCommandMixin
from ..models.payment import PaymentResponse


class PaymentClient(
    CreateCommandMixin[PaymentResponse],
    FindAllCommandMixin[PaymentResponse],
    FindCommandMixin[PaymentResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "payments"
    RESPONSE_MODEL: ClassVar[Type[PaymentResponse]] = PaymentResponse
    ROOT_NAME: ClassVar[str] = "payment"
