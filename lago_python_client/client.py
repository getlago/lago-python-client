from urllib.parse import urljoin

from .services.rate_limit import RateLimitRetryConfig
from .activity_logs.clients import ActivityLogClient
from .add_ons.clients import AddOnClient
from .api_logs.clients import ApiLogClient
from .billable_metrics.clients import BillableMetricClient
from .billing_entities.clients import BillingEntityClient
from .coupons.clients import AppliedCouponClient, CouponClient
from .credit_notes.clients import CreditNoteClient
from .customers.applied_coupons_client import CustomerAppliedCouponsClient
from .customers.clients import CustomerClient
from .customers.credit_notes_client import CustomerCreditNotesClient
from .customers.invoices_client import CustomerInvoicesClient
from .customers.payment_methods_client import CustomerPaymentMethodsClient
from .customers.payment_requests_client import CustomerPaymentRequestsClient
from .customers.payments_client import CustomerPaymentsClient
from .customers.subscriptions_client import CustomerSubscriptionsClient
from .customers.wallets_client import CustomerWalletsClient
from .events.clients import EventClient
from .fees.clients import FeeClient
from .functools_ext import callable_cached_property
from .gross_revenues.clients import GrossRevenueClient
from .invoice_collections.clients import InvoiceCollectionClient
from .invoiced_usages.clients import InvoicedUsageClient
from .invoices.clients import InvoiceClient
from .mrrs.clients import MrrClient
from .organizations.clients import OrganizationClient
from .overdue_balances.clients import OverdueBalanceClient
from .payment_receipts.clients import PaymentReceiptClient
from .payment_requests.clients import PaymentRequestClient
from .payments.clients import PaymentClient
from .plans.charges_client import PlanChargesClient
from .plans.clients import PlanClient
from .plans.fixed_charges_client import PlanFixedChargesClient
from .subscriptions.charges_client import SubscriptionChargesClient
from .subscriptions.clients import SubscriptionClient
from .subscriptions.fixed_charges_client import SubscriptionFixedChargesClient
from .taxes.clients import TaxClient
from .usages.clients import UsageClient
from .wallets.clients import WalletClient, WalletTransactionClient
from .webhook_endpoints.clients import WebhookEndpointClient
from .webhooks.clients import WebhookClient

try:
    from typing import Final
except ImportError:  # Python 3.7
    from typing_extensions import Final  # type: ignore


class Client:
    BASE_URL: Final[str] = "https://api.getlago.com/"
    BASE_INGEST_URL: Final[str] = "https://ingest.getlago.com/"
    API_PATH: Final[str] = "api/v1/"

    def __init__(
        self,
        api_key: str = "",
        api_url: str = "",
        use_ingest_service: bool = False,
        ingest_api_url: str = "",
        max_retries: int = 3,
        retry_on_rate_limit: bool = True,
    ) -> None:
        self.api_key: str = api_key
        self.api_url: str = api_url
        self.use_ingest_service: bool = use_ingest_service
        self.ingest_api_url: str = ingest_api_url
        self.rate_limit_retry_config: RateLimitRetryConfig = RateLimitRetryConfig(
            max_retries=max_retries,
            retry_on_rate_limit=retry_on_rate_limit,
        )

    @property
    def base_api_url(self) -> str:
        return urljoin(self.api_url if self.api_url else Client.BASE_URL, Client.API_PATH)

    @property
    def base_ingest_api_url(self) -> str:
        if not self.use_ingest_service:
            return self.base_api_url

        if self.ingest_api_url == "":
            ingest_url = Client.BASE_INGEST_URL
        else:
            ingest_url = self.ingest_api_url

        return urljoin(ingest_url, Client.API_PATH)

    def _create_client(self, client_class, base_url, api_key, base_ingest_url=""):
        """Create a client instance with rate limit config."""
        if base_ingest_url:
            return client_class(base_url, api_key, base_ingest_url, self.rate_limit_retry_config)
        return client_class(base_url, api_key, rate_limit_retry_config=self.rate_limit_retry_config)

    @callable_cached_property
    def add_ons(self) -> AddOnClient:
        return self._create_client(AddOnClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def billable_metrics(self) -> BillableMetricClient:
        return self._create_client(BillableMetricClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def billing_entities(self) -> BillingEntityClient:
        return self._create_client(BillingEntityClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def coupons(self) -> CouponClient:
        return self._create_client(CouponClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def applied_coupons(self) -> AppliedCouponClient:
        return self._create_client(AppliedCouponClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def credit_notes(self) -> CreditNoteClient:
        return self._create_client(CreditNoteClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customers(self) -> CustomerClient:
        return self._create_client(CustomerClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_applied_coupons(self) -> CustomerAppliedCouponsClient:
        return self._create_client(CustomerAppliedCouponsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_credit_notes(self) -> CustomerCreditNotesClient:
        return self._create_client(CustomerCreditNotesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_invoices(self) -> CustomerInvoicesClient:
        return self._create_client(CustomerInvoicesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_payment_methods(self) -> CustomerPaymentMethodsClient:
        return self._create_client(CustomerPaymentMethodsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_payments(self) -> CustomerPaymentsClient:
        return self._create_client(CustomerPaymentsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_payment_requests(self) -> CustomerPaymentRequestsClient:
        return self._create_client(CustomerPaymentRequestsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_subscriptions(self) -> CustomerSubscriptionsClient:
        return self._create_client(CustomerSubscriptionsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def customer_wallets(self) -> CustomerWalletsClient:
        return self._create_client(CustomerWalletsClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def events(self) -> EventClient:
        return self._create_client(EventClient, self.base_api_url, self.api_key, self.base_ingest_api_url)

    @callable_cached_property
    def fees(self) -> FeeClient:
        return self._create_client(FeeClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def gross_revenues(self) -> GrossRevenueClient:
        return self._create_client(GrossRevenueClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def invoices(self) -> InvoiceClient:
        return self._create_client(InvoiceClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def invoiced_usages(self) -> InvoicedUsageClient:
        return self._create_client(InvoicedUsageClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def mrrs(self) -> MrrClient:
        return self._create_client(MrrClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def organizations(self) -> OrganizationClient:
        return self._create_client(OrganizationClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def overdue_balances(self) -> OverdueBalanceClient:
        return self._create_client(OverdueBalanceClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def payment_receipts(self) -> PaymentReceiptClient:
        return self._create_client(PaymentReceiptClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def payment_requests(self) -> PaymentRequestClient:
        return self._create_client(PaymentRequestClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def payments(self) -> PaymentClient:
        return self._create_client(PaymentClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def invoice_collections(self) -> InvoiceCollectionClient:
        return self._create_client(InvoiceCollectionClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def plans(self) -> PlanClient:
        return self._create_client(PlanClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def plan_charges(self) -> PlanChargesClient:
        return self._create_client(PlanChargesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def plan_fixed_charges(self) -> PlanFixedChargesClient:
        return self._create_client(PlanFixedChargesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def subscriptions(self) -> SubscriptionClient:
        return self._create_client(SubscriptionClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def subscription_charges(self) -> SubscriptionChargesClient:
        return self._create_client(SubscriptionChargesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def subscription_fixed_charges(self) -> SubscriptionFixedChargesClient:
        return self._create_client(SubscriptionFixedChargesClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def taxes(self) -> TaxClient:
        return self._create_client(TaxClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def usages(self) -> UsageClient:
        return self._create_client(UsageClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def wallets(self) -> WalletClient:
        return self._create_client(WalletClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def wallet_transactions(self) -> WalletTransactionClient:
        return self._create_client(WalletTransactionClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def webhooks(self) -> WebhookClient:
        return self._create_client(WebhookClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def webhook_endpoints(self) -> WebhookEndpointClient:
        return self._create_client(WebhookEndpointClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def activity_logs(self) -> ActivityLogClient:
        return self._create_client(ActivityLogClient, self.base_api_url, self.api_key)

    @callable_cached_property
    def api_logs(self) -> ApiLogClient:
        return self._create_client(ApiLogClient, self.base_api_url, self.api_key)
