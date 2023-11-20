import sys
from typing import Any, Mapping, ClassVar, Type, Union

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin
from ..models.customer import CustomerResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.request import make_headers, make_url, send_get_request, send_post_request
from ..services.response import get_response_data, prepare_index_response, prepare_object_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


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

    def past_usage(self, resource_id: str, external_subscription_id: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'past_usage'),
                query_pairs={
                    'external_subscription_id': external_subscription_id,
                    **options,
                },
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource='usage_periods',
            response_model=CustomerUsageResponse,
            data=get_response_data(response=api_response),
        )


    def portal_url(self, resource_id: str) -> str:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'portal_url'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        return response_data.get('portal_url', '') if isinstance(response_data, Mapping) else ''

    def checkout_url(self, resource_id: str) -> str:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'checkout_url'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        return response_data.get('checkout_url', '') if isinstance(response_data, Mapping) else ''