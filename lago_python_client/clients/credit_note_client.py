import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.credit_note import CreditNoteResponse
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import prepare_object_response, verify_response


class CreditNoteClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'credit_notes'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = CreditNoteResponse
    ROOT_NAME: ClassVar[str] = 'credit_note'

    def download(self, resource_id: str):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'download'),
        )
        api_response: Response = requests.post(query_url, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True
        else:
            return prepare_object_response(response_model=self.RESPONSE_MODEL, data=from_json(data).get(self.ROOT_NAME))

    def void(self, resource_id: str):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id, 'void'),
        )
        api_response: Response = requests.put(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return prepare_object_response(response_model=self.RESPONSE_MODEL, data=data)
