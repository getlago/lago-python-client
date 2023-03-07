import requests
from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.invoice import InvoiceResponse
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


class InvoiceClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def download(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'download'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.post(query_url, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_object_response(from_json(data).get(self.ROOT_NAME))

    def retry_payment(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'retry_payment'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.post(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_object_response(data)

    def refresh(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'refresh'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_object_response(data)

    def finalize(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'finalize'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_object_response(data)
