import requests
from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.customer import CustomerResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.request import make_url
from ..services.response import get_response_data, prepare_object_response, Response


class CustomerClient(
    CreateCommandMixin[CustomerResponse],
    DestroyCommandMixin[CustomerResponse],
    FindAllCommandMixin[CustomerResponse],
    FindCommandMixin[CustomerResponse],
    UpdateCommandMixin[CustomerResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[CustomerResponse]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'

    def current_usage(self, resource_id: str, external_subscription_id: str) -> CustomerUsageResponse:
        api_response: Response = requests.get(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, 'current_usage'),
                query_pairs={
                    'external_subscription_id': external_subscription_id,
                },
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=CustomerUsageResponse,
            data=get_response_data(response=api_response, key='customer_usage'),
        )
