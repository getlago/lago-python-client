from .base_client import BaseClient
from lago_python_client.models.organization import OrganizationResponse
from typing import Dict


class OrganizationClient(BaseClient):
    def api_resource(self):
        return 'organizations'

    def root_name(self):
        return 'organization'

    def prepare_response(self, data: Dict):
        return OrganizationResponse.parse_obj(data)
