import requests

from .base_client import BaseClient
from lago_python_client.models.customer import CustomerResponse
from lago_python_client.models.customer_usage import CustomerUsageResponse
from typing import Dict
from urllib.parse import urljoin


class CustomerClient(BaseClient):
    def api_resource(self):
        return 'customers'

    def root_name(self):
        return 'customer'

    def prepare_response(self, data: Dict):
        return CustomerResponse.parse_obj(data)

    def current_usage(self, resource_id: str, external_subscription_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/current_usage?external_subscription_id=' + external_subscription_id
        query_url = urljoin(self.base_url, api_resource)

        api_response = requests.get(query_url, headers=self.headers())
        data = self.handle_response(api_response).json().get('customer_usage')

        return CustomerUsageResponse.parse_obj(data)
