from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.applied_add_on import AppliedAddOnResponse


class AppliedAddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedAddOnResponse
    ROOT_NAME: ClassVar[str] = 'applied_add_on'

    def prepare_response(self, data: Dict[Any, Any]) -> BaseModel:
        return self.RESPONSE_MODEL.parse_obj(data)
