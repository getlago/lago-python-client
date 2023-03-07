from typing import ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.plan import PlanResponse


class PlanClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'plans'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = PlanResponse
    ROOT_NAME: ClassVar[str] = 'plan'

    def prepare_response(self, data: Dict):
        return self.RESPONSE_MODEL.parse_obj(data)
