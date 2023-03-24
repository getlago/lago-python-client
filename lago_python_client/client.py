from urllib.parse import urljoin

from .add_ons import clients as add_ons_clients
from .billable_metrics import clients as billable_metrics_clients
from .coupons import clients as coupons_clients
from .credit_notes import clients as credit_notes_clients
from .customers import clients as customers_clients
from .events import clients as events_clients
from .fees import clients as fees_clients
from .functools_ext import callable_cached_property
from .invoices import clients as invoices_clients
from .organizations import clients as organizations_clients
from .plans import clients as plans_clients
from .subscriptions import clients as subscriptions_clients
from .wallets import clients as wallets_clients
from .webhooks import clients as webhooks_clients

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
    def applied_add_ons(self) -> add_ons_clients.AppliedAddOnClient:
        return add_ons_clients.AppliedAddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def add_ons(self) -> add_ons_clients.AddOnClient:
        return add_ons_clients.AddOnClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def billable_metrics(self) -> billable_metrics_clients.BillableMetricClient:
        return billable_metrics_clients.BillableMetricClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def groups(self) -> billable_metrics_clients.GroupClient:
        return billable_metrics_clients.GroupClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def coupons(self) -> coupons_clients.CouponClient:
        return coupons_clients.CouponClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def applied_coupons(self) -> coupons_clients.AppliedCouponClient:
        return coupons_clients.AppliedCouponClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def credit_notes(self) -> credit_notes_clients.CreditNoteClient:
        return credit_notes_clients.CreditNoteClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def customers(self) -> customers_clients.CustomerClient:
        return customers_clients.CustomerClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def events(self) -> events_clients.EventClient:
        return events_clients.EventClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def fees(self) -> fees_clients.FeeClient:
        return fees_clients.FeeClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def invoices(self) -> invoices_clients.InvoiceClient:
        return invoices_clients.InvoiceClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def organizations(self) -> organizations_clients.OrganizationClient:
        return organizations_clients.OrganizationClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def plans(self) -> plans_clients.PlanClient:
        return plans_clients.PlanClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def subscriptions(self) -> subscriptions_clients.SubscriptionClient:
        return subscriptions_clients.SubscriptionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallets(self) -> wallets_clients.WalletClient:
        return wallets_clients.WalletClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def wallet_transactions(self) -> wallets_clients.WalletTransactionClient:
        return wallets_clients.WalletTransactionClient(self.base_api_url, self.api_key)

    @callable_cached_property
    def webhooks(self) -> webhooks_clients.WebhookClient:
        return webhooks_clients.WebhookClient(self.base_api_url, self.api_key)
