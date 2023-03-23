from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin
from ..models.customer import CustomerResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_object_response, Response


class CustomerClient(
    CreateCommandMixin[CustomerResponse],
    DestroyCommandMixin[CustomerResponse],
    FindAllCommandMixin[CustomerResponse],
    FindCommandMixin[CustomerResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'

    def current_usage(self, resource_id: str, external_subscription_id: str) -> CustomerUsageResponse:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'current_usage'),
                query_pairs={
                    'external_subscription_id': external_subscription_id,
                },
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=CustomerUsageResponse,
            data=get_response_data(response=api_response, key='customer_usage'),
        )
