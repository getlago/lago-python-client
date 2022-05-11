from .base_client import BaseClient
from lago_python_client.models.customer import ResponseCustomer
from typing import Dict


class CustomerClient(BaseClient):
    def api_resource(self):
        return 'customers'

    def root_name(self):
        return 'customer'

    def prepare_response(self, data: Dict):
        return ResponseCustomer.parse_obj(data)
