from lago_python_client.clients.applied_add_on_client import AppliedAddOnClient
from lago_python_client.clients.applied_coupon_client import AppliedCouponClient
from lago_python_client.clients.billable_metric_client import BillableMetricClient
from lago_python_client.clients.coupon_client import CouponClient
from lago_python_client.clients.group_client import GroupClient
from lago_python_client.clients.credit_note_client import CreditNoteClient
from lago_python_client.clients.plan_client import PlanClient
from lago_python_client.clients.add_on_client import AddOnClient
from lago_python_client.clients.organization_client import OrganizationClient
from lago_python_client.clients.subscription_client import SubscriptionClient
from lago_python_client.clients.customer_client import CustomerClient
from lago_python_client.clients.invoice_client import InvoiceClient
from lago_python_client.clients.event_client import EventClient
from lago_python_client.clients.webhook_client import WebhookClient
from lago_python_client.clients.wallet_client import WalletClient
from lago_python_client.clients.wallet_transaction_client import WalletTransactionClient
from urllib.parse import urljoin
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

    def base_api_url(self) -> str:
        if self.api_url:
            return urljoin(self.api_url, Client.API_PATH)
        else:
            return urljoin(Client.BASE_URL, Client.API_PATH)

    def events(self) -> EventClient:
        return EventClient(self.base_api_url(), self.api_key)

    def groups(self) -> GroupClient:
        return GroupClient(self.base_api_url(), self.api_key)

    def subscriptions(self) -> SubscriptionClient:
        return SubscriptionClient(self.base_api_url(), self.api_key)

    def credit_notes(self) -> CreditNoteClient:
        return CreditNoteClient(self.base_api_url(), self.api_key)

    def customers(self) -> CustomerClient:
        return CustomerClient(self.base_api_url(), self.api_key)

    def invoices(self) -> InvoiceClient:
        return InvoiceClient(self.base_api_url(), self.api_key)

    def applied_coupons(self) -> AppliedCouponClient:
        return AppliedCouponClient(self.base_api_url(), self.api_key)

    def applied_add_ons(self) -> AppliedAddOnClient:
        return AppliedAddOnClient(self.base_api_url(), self.api_key)

    def billable_metrics(self) -> BillableMetricClient:
        return BillableMetricClient(self.base_api_url(), self.api_key)

    def coupons(self) -> CouponClient:
        return CouponClient(self.base_api_url(), self.api_key)

    def plans(self) -> PlanClient:
        return PlanClient(self.base_api_url(), self.api_key)

    def add_ons(self) -> AddOnClient:
        return AddOnClient(self.base_api_url(), self.api_key)

    def organizations(self) -> OrganizationClient:
        return OrganizationClient(self.base_api_url(), self.api_key)

    def webhooks(self) -> WebhookClient:
        return WebhookClient(self.base_api_url(), self.api_key)

    def wallets(self) -> WalletClient:
        return WalletClient(self.base_api_url(), self.api_key)

    def wallet_transactions(self) -> WalletTransactionClient:
        return WalletTransactionClient(self.base_api_url(), self.api_key)
