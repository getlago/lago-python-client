from .base_client import BaseClient
from lago_python_client.models.subscription import SubscriptionResponse
from typing import Dict


class SubscriptionClient(BaseClient):
    def api_resource(self):
        return 'subscriptions'

    def root_name(self):
        return 'subscription'

    def prepare_response(self, data: Dict):
        return SubscriptionResponse.parse_obj(data)
