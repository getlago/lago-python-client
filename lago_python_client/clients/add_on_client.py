from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.add_on import AddOnResponse


class AddOnClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'add_ons'
    ROOT_NAME: ClassVar[str] = 'add_on'

    def prepare_response(self, data: Dict):
        return AddOnResponse.parse_obj(data)
