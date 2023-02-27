from urllib.parse import urljoin

from .clients.applied_add_on_client import AppliedAddOnClient
from .clients.applied_coupon_client import AppliedCouponClient
from .clients.billable_metric_client import BillableMetricClient
from .clients.coupon_client import CouponClient
from .clients.group_client import GroupClient
from .clients.credit_note_client import CreditNoteClient
from .clients.plan_client import PlanClient
from .clients.add_on_client import AddOnClient
from .clients.organization_client import OrganizationClient
from .clients.subscription_client import SubscriptionClient
from .clients.customer_client import CustomerClient
from .clients.invoice_client import InvoiceClient
from .clients.event_client import EventClient
from .clients.fee_client import FeeClient
from .clients.webhook_client import WebhookClient
from .clients.wallet_client import WalletClient
from .clients.wallet_transaction_client import WalletTransactionClient
from .functools_ext import callable_cached_property

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

    @callable_cached_property
    def events(self) -> EventClient:
        return EventClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def fees(self) -> FeeClient:
        return FeeClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def groups(self) -> GroupClient:
        return GroupClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def subscriptions(self) -> SubscriptionClient:
        return SubscriptionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def credit_notes(self) -> CreditNoteClient:
        return CreditNoteClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def customers(self) -> CustomerClient:
        return CustomerClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoices(self) -> InvoiceClient:
        return InvoiceClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def applied_coupons(self) -> AppliedCouponClient:
        return AppliedCouponClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def applied_add_ons(self) -> AppliedAddOnClient:
        return AppliedAddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def billable_metrics(self) -> BillableMetricClient:
        return BillableMetricClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def coupons(self) -> CouponClient:
        return CouponClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def plans(self) -> PlanClient:
        return PlanClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def add_ons(self) -> AddOnClient:
        return AddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def organizations(self) -> OrganizationClient:
        return OrganizationClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def webhooks(self) -> WebhookClient:
        return WebhookClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallets(self) -> WalletClient:
        return WalletClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallet_transactions(self) -> WalletTransactionClient:
        return WalletTransactionClient(self.base_api_url, self.api_key)
