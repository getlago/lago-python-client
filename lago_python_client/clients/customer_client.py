import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.customer import CustomerResponse
from ..models.customer_usage import CustomerUsageResponse
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import verify_response


class CustomerClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'customers'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = CustomerResponse
    ROOT_NAME: ClassVar[str] = 'customer'

    def current_usage(self, resource_id: str, external_subscription_id: str):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'current_usage'),
            query_pairs={
                'external_subscription_id': external_subscription_id,
            },
        )
        api_response: Response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get('customer_usage')

        return CustomerUsageResponse.parse_obj(data)
