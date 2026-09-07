from typing import Any, ClassVar, Mapping, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import DEFAULT_TIMEOUT, CreateCommandMixin, FindAllCommandMixin, FindCommandMixin
from ..models.payment import PaymentResponse
from ..services.request import QueryPairs
from .filters import payment_filter_options


class PaymentClient(
    CreateCommandMixin[PaymentResponse],
    FindAllCommandMixin[PaymentResponse],
    FindCommandMixin[PaymentResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "payments"
    RESPONSE_MODEL: ClassVar[Type[PaymentResponse]] = PaymentResponse
    ROOT_NAME: ClassVar[str] = "payment"

    def find_all(
        self, options: QueryPairs = None, timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT
    ) -> Mapping[str, Any]:
        """List payments using PaymentFilters or query pairs.

        Accepted keys: page, per_page, external_customer_id, invoice_id, payment_status
        (or payment_statuses), amount_from, amount_to, receipt_number, created_at_from,
        created_at_to, payment_provider_type, payment_method_type, currency,
        invoice_number, payment_type, payable_type and search_term.
        Enum filters accept a string or list; lists use repeated bracketed query keys.
        Amount bounds are inclusive integer cents (0 through 9223372036854775807).
        """
        return super().find_all(payment_filter_options(options), timeout)
