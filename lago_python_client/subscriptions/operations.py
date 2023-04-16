import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.subscription import SubscriptionResponse
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateSubscription(CreateCommandMixin[SubscriptionResponse], BaseOperation):
    """Assign a plan to a customer."""

    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'


class DestroySubscription(DestroyCommandMixin[SubscriptionResponse], BaseOperation):
    """Terminate a subscription."""

    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'


class FindAllSubscriptions(FindAllCommandMixin[SubscriptionResponse], BaseOperation):
    """Find subscriptions."""

    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'


class UpdateSubscription(UpdateCommandMixin[SubscriptionResponse], BaseOperation):
    """Update an existing subscription."""

    API_RESOURCE: ClassVar[str] = 'subscriptions'
    RESPONSE_MODEL: ClassVar[Type[SubscriptionResponse]] = SubscriptionResponse
    ROOT_NAME: ClassVar[str] = 'subscription'


subscriptions_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateSubscription,
    'destroy': DestroySubscription,
    'find_all': FindAllSubscriptions,
    'update': UpdateSubscription,
}
