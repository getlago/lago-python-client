from .base_client import BaseClient


class SubscriptionClient(BaseClient):
    def api_resource(self):
        return 'subscriptions'

    def root_name(self):
        return 'subscription'
