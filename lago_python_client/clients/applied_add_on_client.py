from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.applied_add_on import AppliedAddOnResponse


class AppliedAddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_add_ons'
    ROOT_NAME: ClassVar[str] = 'applied_add_on'

    def prepare_response(self, data: Dict):
        return AppliedAddOnResponse.parse_obj(data)
