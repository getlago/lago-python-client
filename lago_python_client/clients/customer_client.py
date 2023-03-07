import requests
from typing import Any, ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.customer import CustomerResponse
from lago_python_client.models.customer_usage import CustomerUsageResponse
from urllib.parse import urljoin, urlencode
from ..services.json import from_json
from ..services.response import verify_response


class CustomerClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'customers'
    ROOT_NAME: ClassVar[str] = 'customer'

    def prepare_response(self, data: Dict):
        return CustomerResponse.parse_obj(data)

    def current_usage(self, resource_id: str, external_subscription_id: str):
        options: Dict[str, Any] = {
            'external_subscription_id': external_subscription_id,
        }
        uri: str = '{uri_path}{uri_query}'.format(
            uri_path='/'.join((self.API_RESOURCE, resource_id, 'current_usage')),
            uri_query=f'?{urlencode(options)}',
        )
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get('customer_usage')

        return CustomerUsageResponse.parse_obj(data)
