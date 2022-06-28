from .base_client import BaseClient
from lago_python_client.models.event import EventResponse
from typing import Dict


class EventClient(BaseClient):
    def api_resource(self):
        return 'events'

    def root_name(self):
        return 'event'

    def prepare_response(self, data: Dict):
        return EventResponse.parse_obj(data)
