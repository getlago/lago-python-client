from .base_client import BaseClient
from lago_python_client.models.add_on import AddOnResponse
from typing import Dict


class AddOnClient(BaseClient):
    def api_resource(self):
        return 'add_ons'

    def root_name(self):
        return 'add_on'

    def prepare_response(self, data: Dict):
        return AddOnResponse.parse_obj(data)
