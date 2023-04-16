from urllib.parse import urljoin

from .add_ons.operations import add_ons_operations_config, applied_add_ons_operations_config
from .billable_metrics.operations import billable_metrics_operations_config, groups_operations_config
from .coupons.operations import coupons_operations_config, applied_coupons_operations_config
from .credit_notes.operations import credit_notes_operations_config
from .customers.operations import customers_operations_config
from .events.operations import events_operations_config
from .fees.operations import fees_operations_config
from .functools_ext import callable_cached_property
from .invoices.operations import invoices_operations_config
from .organizations.operations import organizations_operations_config
from .plans.operations import plans_operations_config
from .subscriptions.operations import subscriptions_operations_config
from .tag_manager import TagManager
from .wallets.operations import wallets_operations_config, wallet_transactions_operations_config
from .webhooks.operations import webhooks_operations_config

try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore


class Client:
    """Lago Client."""

    BASE_URL: Final[str] = 'https://api.getlago.com/'
    API_PATH: Final[str] = 'api/v1/'

    def __init__(self, api_key: str = '', api_url: str = '') -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url

    @property
    def base_api_url(self) -> str:
        return urljoin(self.api_url if self.api_url else Client.BASE_URL, Client.API_PATH)

    @callable_cached_property
    def applied_add_ons(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=applied_add_ons_operations_config)

    @callable_cached_property
    def add_ons(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=add_ons_operations_config)

    @callable_cached_property
    def billable_metrics(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=billable_metrics_operations_config)

    @callable_cached_property
    def groups(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=groups_operations_config)

    @callable_cached_property
    def coupons(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=coupons_operations_config)

    @callable_cached_property
    def applied_coupons(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=applied_coupons_operations_config)

    @callable_cached_property
    def credit_notes(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=credit_notes_operations_config)

    @callable_cached_property
    def customers(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=customers_operations_config)

    @callable_cached_property
    def events(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=events_operations_config)

    @callable_cached_property
    def fees(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=fees_operations_config)

    @callable_cached_property
    def invoices(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=invoices_operations_config)

    @callable_cached_property
    def organizations(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=organizations_operations_config)

    @callable_cached_property
    def plans(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=plans_operations_config)

    @callable_cached_property
    def subscriptions(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=subscriptions_operations_config)

    @callable_cached_property
    def wallets(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=wallets_operations_config)

    @callable_cached_property
    def wallet_transactions(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=wallet_transactions_operations_config)

    @callable_cached_property
    def webhooks(self) -> TagManager:
        return TagManager(base_url=self.base_api_url, api_key=self.api_key, operations=webhooks_operations_config)
