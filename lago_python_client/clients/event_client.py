import requests
from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.event import EventResponse
from urllib.parse import urljoin
from ..services.json import to_json
from ..services.response import verify_response


class EventClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def batch_create(self, input_object: BaseModel):
        uri: str = '/'.join((self.API_RESOURCE, 'batch'))
        query_url: str = urljoin(self.base_url, uri)

        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        data = to_json(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        verify_response(api_response)

        return True

    @classmethod
    def prepare_object_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
