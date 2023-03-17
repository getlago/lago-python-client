from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from ..models.subscription import SubscriptionResponse


class SubscriptionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'
