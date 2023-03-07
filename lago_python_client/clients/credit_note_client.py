import requests
from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.credit_note import CreditNoteResponse
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


class CreditNoteClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def prepare_response(self, data: Dict[Any, Any]) -> BaseModel:
        return self.RESPONSE_MODEL.parse_obj(data)

    def download(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'download'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.post(query_url, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(from_json(data).get(self.ROOT_NAME))

    def void(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id, 'void'))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_response(data)
