from typing import ClassVar, Type

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.subscription import SubscriptionResponse


class SubscriptionClient(CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'
