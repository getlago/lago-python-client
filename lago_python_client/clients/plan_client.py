from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.plan import PlanResponse


class PlanClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'plans'
    ROOT_NAME: ClassVar[str] = 'plan'

    def prepare_response(self, data: Dict):
        return PlanResponse.parse_obj(data)
