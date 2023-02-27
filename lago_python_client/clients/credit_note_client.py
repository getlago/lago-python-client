import requests

from .base_client import BaseClient
from lago_python_client.models.credit_note import CreditNoteResponse
from typing import Dict
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json

class CreditNoteClient(BaseClient):
    def api_resource(self):
        return 'credit_notes'

    def root_name(self):
        return 'credit_note'

    def prepare_response(self, data: Dict):
        return CreditNoteResponse.parse_obj(data)

    def download(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/download'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.post(query_url, headers=self.headers())
        data = self.handle_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(from_json(data).get(self.root_name()))

    def void(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id + '/void'
        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(self.handle_response(api_response)).get(self.root_name())

        return self.prepare_response(data)
