from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllCommandMixin, FindCommandMixin
from ..models.payment_receipt import PaymentReceiptResponse


class PaymentReceiptClient(
    FindAllCommandMixin[PaymentReceiptResponse],
    FindCommandMixin[PaymentReceiptResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "payment_receipts"
    RESPONSE_MODEL: ClassVar[Type[PaymentReceiptResponse]] = PaymentReceiptResponse
    ROOT_NAME: ClassVar[str] = "payment_receipt"
