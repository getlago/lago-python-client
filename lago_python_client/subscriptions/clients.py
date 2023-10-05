from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.subscription import SubscriptionResponse


class SubscriptionClient(
    CreateCommandMixin[SubscriptionResponse],
    DestroyCommandMixin[SubscriptionResponse],
    FindAllCommandMixin[SubscriptionResponse],
    FindCommandMixin[SubscriptionResponse],
    UpdateCommandMixin[SubscriptionResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'
