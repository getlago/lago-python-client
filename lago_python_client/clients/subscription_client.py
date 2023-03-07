from typing import ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.subscription import SubscriptionResponse


class SubscriptionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'

    def prepare_response(self, data: Dict):
        return self.RESPONSE_MODEL.parse_obj(data)
