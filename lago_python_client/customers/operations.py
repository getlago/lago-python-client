import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.customer import CustomerResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_object_response, Response
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateCustomer(CreateCommandMixin[CustomerResponse], BaseOperation):
    """Create a customer."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'


class DeleteCustomer(DestroyCommandMixin[CustomerResponse], BaseOperation):
    """Delete a customer."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'


class FindAllCustomers(FindAllCommandMixin[CustomerResponse], BaseOperation):
    """Find customers."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'


class FindCustomer(FindCommandMixin[CustomerResponse], BaseOperation):
    """Find customer by external ID."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'


class FindCustomerCurrentUsage(BaseOperation):
    """Find customer current usage."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'

    def __call__(self, resource_id: str, external_subscription_id: str) -> CustomerUsageResponse:
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


class GetCustomerPortalUrl(BaseOperation):
    """Get customer portal URL."""

    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'

    def __call__(self, resource_id: str) -> str:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'portal_url'),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        return response_data.get('portal_url', '') if isinstance(response_data, Mapping) else ''


customers_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateCustomer,
    'current_usage': FindCustomerCurrentUsage,
    'destroy': DeleteCustomer,
    'find': FindCustomer,
    'find_all': FindAllCustomers,
    'portal_url': GetCustomerPortalUrl,
}
