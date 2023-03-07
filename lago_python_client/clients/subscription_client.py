from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.subscription import SubscriptionResponse


class SubscriptionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'

    @classmethod
    def prepare_object_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
