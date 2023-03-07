from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.organization import OrganizationResponse


class OrganizationClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'organizations'
    ROOT_NAME: ClassVar[str] = 'organization'

    def prepare_response(self, data: Dict):
        return OrganizationResponse.parse_obj(data)
