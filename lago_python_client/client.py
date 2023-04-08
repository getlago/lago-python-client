from urllib.parse import urljoin
import warnings

from .add_ons.clients import AddOnClient, AppliedAddOnClient
from .billable_metrics.clients import BillableMetricClient, GroupClient
from .coupons.clients import AppliedCouponClient, CouponClient
from .credit_notes.clients import CreditNoteClient
from .customers.clients import CustomerClient
from .events.clients import EventClient
from .fees.clients import FeeClient
from .functools_ext import callable_cached_property
from .invoices.clients import InvoiceClient
from .organizations.clients import OrganizationClient
from .plans.clients import PlanClient
from .subscriptions.clients import SubscriptionClient
from .wallets.clients import WalletClient, WalletTransactionClient
from .webhooks.clients import WebhookClient

try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore


class Client:
    BASE_URL: Final[str] = 'https://api.getlago.com/'
    API_PATH: Final[str] = 'api/v1/'

    def __init__(self, api_key: str = '', api_url: str = '') -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url

    @property
    def base_api_url(self) -> str:
        return urljoin(self.api_url if self.api_url else Client.BASE_URL, Client.API_PATH)

    # TODO: Deprecate me (replace PendingDeprecationWarning to DeprecationWarning, set date)
    @callable_cached_property
    def applied_add_ons(self) -> AppliedAddOnClient:
        warnings.warn('Use `client.add_ons.apply(...)` instead of `client.applied_add_ons.create(...)`', PendingDeprecationWarning)
        return self.add_ons._applied_add_ons

    @callable_cached_property
    def add_ons(self) -> AddOnClient:
        return AddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def billable_metrics(self) -> BillableMetricClient:
        return BillableMetricClient(self.base_api_url, self.api_key)

    # TODO: Deprecate me (replace PendingDeprecationWarning to DeprecationWarning, set date)
    @callable_cached_property
    def groups(self) -> GroupClient:
        warnings.warn('Use `client.billable_metrics.find_all_groups(...)` instead of `client.groups.find_all(...)`', PendingDeprecationWarning)
        return self.billable_metrics._groups

    @callable_cached_property
    def coupons(self) -> CouponClient:
        return CouponClient(self.base_api_url, self.api_key)

    # TODO: Deprecate me (replace PendingDeprecationWarning to DeprecationWarning, set date)
    @callable_cached_property
    def applied_coupons(self) -> AppliedCouponClient:
        warnings.warn(
            ''.join((
                'Use `client.coupons.apply(...)` / `client.coupons.find_all_applied(...)` / `client.coupons.delete_applied(...)` instead of ',
                '`client.applied_coupons.create(...)` / `client.applied_coupons.find_all(...)` / `client.applied_coupons.destroy(...)`',
            )),
            PendingDeprecationWarning,
        )
        return self.coupons._applied_coupons

    @callable_cached_property
    def credit_notes(self) -> CreditNoteClient:
        return CreditNoteClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def customers(self) -> CustomerClient:
        return CustomerClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def events(self) -> EventClient:
        return EventClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def fees(self) -> FeeClient:
        return FeeClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoices(self) -> InvoiceClient:
        return InvoiceClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def organizations(self) -> OrganizationClient:
        return OrganizationClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def plans(self) -> PlanClient:
        return PlanClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def subscriptions(self) -> SubscriptionClient:
        return SubscriptionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallets(self) -> WalletClient:
        return WalletClient(self.base_api_url, self.api_key)

    # TODO: Deprecate me (replace PendingDeprecationWarning to DeprecationWarning, set date)
    @callable_cached_property
    def wallet_transactions(self) -> WalletTransactionClient:
        warnings.warn(
            ''.join((
                'Use `client.wallets.create_transaction(...)` / `client.wallets.find_all_transactions(...)` instead of ',
                '`client.wallet_transactions.create(...)` / `client.wallet_transactions.find_all(...)`',
            )),
            PendingDeprecationWarning,
        )
        return self.wallets._wallet_transactions

    @callable_cached_property
    def webhooks(self) -> WebhookClient:
        return WebhookClient(self.base_api_url, self.api_key)
