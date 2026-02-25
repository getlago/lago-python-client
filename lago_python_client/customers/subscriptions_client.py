from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.subscription import SubscriptionResponse
from .clients import CustomerClient


class CustomerSubscriptionsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "subscriptions"
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = "subscription"
