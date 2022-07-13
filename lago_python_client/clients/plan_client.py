from .base_client import BaseClient
from lago_python_client.models.plan import PlanResponse
from typing import Dict


class PlanClient(BaseClient):
    def api_resource(self):
        return 'plans'

    def root_name(self):
        return 'plan'

    def prepare_response(self, data: Dict):
        return PlanResponse.parse_obj(data)
