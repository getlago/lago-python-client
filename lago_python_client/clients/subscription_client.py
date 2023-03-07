from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.subscription import SubscriptionResponse


class SubscriptionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    ROOT_NAME: ClassVar[str] = 'subscription'

    def prepare_response(self, data: Dict):
        return SubscriptionResponse.parse_obj(data)
