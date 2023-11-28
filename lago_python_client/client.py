from urllib.parse import urljoin

from .add_ons.clients import AddOnClient
from .billable_metrics.clients import BillableMetricClient, GroupClient
from .coupons.clients import AppliedCouponClient, CouponClient
from .credit_notes.clients import CreditNoteClient
from .customers.clients import CustomerClient
from .events.clients import EventClient
from .fees.clients import FeeClient
from .functools_ext import callable_cached_property
from .gross_revenues.clients import GrossRevenueClient
from .invoices.clients import InvoiceClient
from .invoiced_usages.clients import InvoicedUsageClient
from .mrrs.clients import MrrClient
from .organizations.clients import OrganizationClient
from .invoice_collections.clients import InvoiceCollectionClient
from .plans.clients import PlanClient
from .subscriptions.clients import SubscriptionClient
from .taxes.clients import TaxClient
from .wallets.clients import WalletClient, WalletTransactionClient
from .webhooks.clients import WebhookClient
from .webhook_endpoints.clients import WebhookEndpointClient

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
    def add_ons(self) -> AddOnClient:
        return AddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def billable_metrics(self) -> BillableMetricClient:
        return BillableMetricClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def groups(self) -> GroupClient:
        return GroupClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def coupons(self) -> CouponClient:
        return CouponClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def applied_coupons(self) -> AppliedCouponClient:
        return AppliedCouponClient(self.base_api_url, self.api_key)

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
    def gross_revenues(self) -> GrossRevenueClient:
        return GrossRevenueClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoices(self) -> InvoiceClient:
        return InvoiceClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoiced_usages(self) -> InvoicedUsageClient:
        return InvoicedUsageClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def mrrs(self) -> MrrClient:
        return MrrClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def organizations(self) -> OrganizationClient:
        return OrganizationClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoice_collections(self) -> InvoiceCollectionClient:
        return InvoiceCollectionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def plans(self) -> PlanClient:
        return PlanClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def subscriptions(self) -> SubscriptionClient:
        return SubscriptionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def taxes(self) -> TaxClient:
        return TaxClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallets(self) -> WalletClient:
        return WalletClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallet_transactions(self) -> WalletTransactionClient:
        return WalletTransactionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def webhooks(self) -> WebhookClient:
        return WebhookClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def webhook_endpoints(self) -> WebhookEndpointClient:
        return WebhookEndpointClient(self.base_api_url, self.api_key)
