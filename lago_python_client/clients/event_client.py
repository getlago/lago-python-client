import requests

from .base_client import BaseClient
from lago_python_client.models.event import EventResponse
from typing import Dict

from pydantic import BaseModel
from urllib.parse import urljoin
from ..services.json import to_json
from ..services.response import verify_response


class EventClient(BaseClient):
    def api_resource(self):
        return 'events'

    def root_name(self):
        return 'event'

    def batch_create(self, input_object: BaseModel):
        api_resource = self.api_resource() + '/batch'
        query_url = urljoin(self.base_url, api_resource)
        query_parameters = {
            self.root_name(): input_object.dict()
        }
        data = to_json(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        verify_response(api_response)

        return True

    def prepare_response(self, data: Dict):
        return EventResponse.parse_obj(data)
