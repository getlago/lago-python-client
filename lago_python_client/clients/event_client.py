import requests
from typing import ClassVar, Optional, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.event import EventResponse
from ..services.json import to_json
from ..services.request import make_url
from ..services.response import verify_response


class EventClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'events'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = EventResponse
    ROOT_NAME: ClassVar[str] = 'event'

    def batch_create(self, input_object: BaseModel) -> Optional[bool]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, 'batch'),
        )
        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        data = to_json(query_parameters)
        api_response: Response = requests.post(query_url, data=data, headers=self.headers())
        verify_response(api_response)

        return True  # TODO: should return None
