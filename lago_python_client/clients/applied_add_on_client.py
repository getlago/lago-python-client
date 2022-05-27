from .base_client import BaseClient
from lago_python_client.models.applied_add_on import AppliedAddOnResponse
from typing import Dict


class AppliedAddOnClient(BaseClient):
    def api_resource(self):
        return 'applied_add_ons'

    def root_name(self):
        return 'applied_add_on'

    def prepare_response(self, data: Dict):
        return AppliedAddOnResponse.parse_obj(data)
