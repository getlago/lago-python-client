from .base_client import BaseClient


class EventClient(BaseClient):
    def api_resource(self):
        return 'events'

    def root_name(self):
        return 'event'
