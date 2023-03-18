import requests
from typing import ClassVar, Optional, Type, Union

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.invoice import InvoiceResponse
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import prepare_object_response, verify_response


class InvoiceClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'invoices'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = 'invoice'

    def download(self, resource_id: str) -> Union[Optional[BaseModel], bool]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'download'),
        )
        api_response: Response = requests.post(query_url, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True  # TODO: should return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(data).get(self.ROOT_NAME),
        )

    def retry_payment(self, resource_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'retry_payment'),
        )
        api_response: Response = requests.post(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def refresh(self, resource_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'refresh'),
        )
        api_response: Response = requests.put(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def finalize(self, resource_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'finalize'),
        )
        api_response: Response = requests.put(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )
