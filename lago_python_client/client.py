from lago_python_client.clients.applied_add_on_client import AppliedAddOnClient
from lago_python_client.clients.applied_coupon_client import AppliedCouponClient
from lago_python_client.clients.billable_metric_client import BillableMetricClient
from lago_python_client.clients.coupon_client import CouponClient
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


class Client:
    BASE_URL = 'https://api.getlago.com/'
    API_PATH = 'api/v1/'

    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url

    def base_api_url(self):
        if self.api_url is None:
            return urljoin(Client.BASE_URL, Client.API_PATH)
        else:
            return urljoin(self.api_url, Client.API_PATH)

    def events(self):
        return EventClient(self.base_api_url(), self.api_key)

    def subscriptions(self):
        return SubscriptionClient(self.base_api_url(), self.api_key)

    def customers(self):
        return CustomerClient(self.base_api_url(), self.api_key)

    def invoices(self):
        return InvoiceClient(self.base_api_url(), self.api_key)

    def applied_coupons(self):
        return AppliedCouponClient(self.base_api_url(), self.api_key)

    def applied_add_ons(self):
        return AppliedAddOnClient(self.base_api_url(), self.api_key)

    def billable_metrics(self):
        return BillableMetricClient(self.base_api_url(), self.api_key)

    def coupons(self):
        return CouponClient(self.base_api_url(), self.api_key)

    def plans(self):
        return PlanClient(self.base_api_url(), self.api_key)

    def add_ons(self):
        return AddOnClient(self.base_api_url(), self.api_key)

    def organizations(self):
        return OrganizationClient(self.base_api_url(), self.api_key)

    def webhooks(self):
        return WebhookClient(self.base_api_url(), self.api_key)

    def wallets(self):
        return WalletClient(self.base_api_url(), self.api_key)

    def wallet_transactions(self):
        return WalletTransactionClient(self.base_api_url(), self.api_key)
