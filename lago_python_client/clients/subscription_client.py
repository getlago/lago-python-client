from .base_client import BaseClient
from lago_python_client.models.subscription import ResponseSubscription
from typing import Dict


class SubscriptionClient(BaseClient):
    def api_resource(self):
        return 'subscriptions'

    def root_name(self):
        return 'subscription'

    def prepare_response(self, data: Dict):
        return ResponseSubscription.parse_obj(data)
