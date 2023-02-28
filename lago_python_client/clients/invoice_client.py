import requests

from .base_client import BaseClient
from lago_python_client.models.invoice import InvoiceResponse
from typing import Dict
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


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
        data = verify_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(from_json(data).get(self.root_name()))

    def retry_payment(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/retry_payment'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.post(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.root_name())

        return self.prepare_response(data)

    def refresh(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/refresh'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.root_name())

        return self.prepare_response(data)

    def finalize(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/finalize'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.root_name())

        return self.prepare_response(data)
