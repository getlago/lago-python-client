import requests

from .base_client import BaseClient
from lago_python_client.models.invoice import InvoiceResponse
from typing import Dict
from urllib.parse import urljoin
from requests import Response


class InvoiceClient(BaseClient):
    def api_resource(self):
        return 'invoices'

    def root_name(self):
        return 'invoice'

    def prepare_response(self, data: Dict):
        return InvoiceResponse.parse_obj(data)

    def download(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/download'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.post(query_url, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)