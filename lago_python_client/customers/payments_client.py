from typing import Any, ClassVar, Mapping, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import DEFAULT_TIMEOUT, FindAllChildrenCommandMixin
from ..models.payment import PaymentResponse
from ..payments.filters import payment_filter_options
from ..services.request import QueryPairs, make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_index_response
from .clients import CustomerClient


class CustomerPaymentsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "payments"
    RESPONSE_MODEL: ClassVar[Type[PaymentResponse]] = PaymentResponse
    ROOT_NAME: ClassVar[str] = "payment"

    def find_all(
        self, resource_id: str, options: QueryPairs = None, timetour: Optional[httpx.Timeout] = None
    ) -> Mapping[str, Any]:
        """List a customer's payments with PaymentFilters; resource_id supplies external_customer_id.

        All other filters and array serialization match PaymentClient.find_all.
        Keep the existing positional and keyword spelling of timetour for compatibility.
        """
        response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.PARENT_API_RESOURCE, resource_id, self.API_RESOURCE),
                query_pairs=payment_filter_options(options),
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timetour if timetour is not None else DEFAULT_TIMEOUT,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )
        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=response),
        )
