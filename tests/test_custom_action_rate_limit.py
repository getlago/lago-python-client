from importlib import import_module
from types import SimpleNamespace

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.exceptions import LagoRateLimitError
from lago_python_client.services.rate_limit import RateLimitRetryConfig

INPUT = SimpleNamespace(dict=lambda **kwargs: {})


@pytest.mark.parametrize(
    "module, client_class, action, args",
    [
        ('lago_python_client.billable_metrics.clients', 'BillableMetricClient', 'evaluate_expression', (INPUT,)),
        ('lago_python_client.coupons.clients', 'AppliedCouponClient', 'destroy', ('test-id', 'test-id')),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'download', ('test-id',)),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'void', ('test-id',)),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'estimate', (INPUT,)),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'replace_metadata', ('test-id', {})),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'merge_metadata', ('test-id', {})),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'delete_all_metadata', ('test-id',)),
        ('lago_python_client.credit_notes.clients', 'CreditNoteClient', 'delete_metadata_key', ('test-id', 'test-id')),
        ('lago_python_client.customers.clients', 'CustomerClient', 'current_usage', ('test-id', 'test-id')),
        ('lago_python_client.customers.clients', 'CustomerClient', 'projected_usage', ('test-id', 'test-id')),
        ('lago_python_client.customers.clients', 'CustomerClient', 'past_usage', ('test-id', 'test-id')),
        ('lago_python_client.customers.clients', 'CustomerClient', 'portal_url', ('test-id',)),
        ('lago_python_client.customers.clients', 'CustomerClient', 'checkout_url', ('test-id',)),
        ('lago_python_client.customers.payment_methods_client', 'CustomerPaymentMethodsClient', 'destroy', ('test-id', 'test-id')),
        ('lago_python_client.customers.payment_methods_client', 'CustomerPaymentMethodsClient', 'set_as_default', ('test-id', 'test-id')),
        ('lago_python_client.customers.wallets.alert_client', 'CustomerWalletAlertClient', 'create_batch', ('test-id', 'test-id', INPUT)),
        ('lago_python_client.customers.wallets.alert_client', 'CustomerWalletAlertClient', 'destroy_all', ('test-id', 'test-id')),
        ('lago_python_client.customers.wallets.metadata_client', 'CustomerWalletMetadataClient', 'replace', ('test-id', 'test-id', {})),
        ('lago_python_client.customers.wallets.metadata_client', 'CustomerWalletMetadataClient', 'merge', ('test-id', 'test-id', {})),
        ('lago_python_client.customers.wallets.metadata_client', 'CustomerWalletMetadataClient', 'delete_all', ('test-id', 'test-id')),
        ('lago_python_client.customers.wallets.metadata_client', 'CustomerWalletMetadataClient', 'delete_key', ('test-id', 'test-id', 'test-id')),
        ('lago_python_client.events.clients', 'EventClient', 'create', (INPUT,)),
        ('lago_python_client.events.clients', 'EventClient', 'batch_create', (INPUT,)),
        ('lago_python_client.events.clients', 'EventClient', 'estimate_fees', (INPUT,)),
        ('lago_python_client.gross_revenues.clients', 'GrossRevenueClient', 'find_all', ()),
        ('lago_python_client.invoice_collections.clients', 'InvoiceCollectionClient', 'find_all', ()),
        ('lago_python_client.invoiced_usages.clients', 'InvoicedUsageClient', 'find_all', ()),
        ('lago_python_client.mrrs.clients', 'MrrClient', 'find_all', ()),
        ('lago_python_client.overdue_balances.clients', 'OverdueBalanceClient', 'find_all', ()),
        ('lago_python_client.plans.clients', 'PlanClient', 'replace_metadata', ('test-id', {})),
        ('lago_python_client.plans.clients', 'PlanClient', 'merge_metadata', ('test-id', {})),
        ('lago_python_client.plans.clients', 'PlanClient', 'delete_all_metadata', ('test-id',)),
        ('lago_python_client.plans.clients', 'PlanClient', 'delete_metadata_key', ('test-id', 'test-id')),
        ('lago_python_client.plans.clients', 'PlanClient', 'find_all_charge_filters', ('test-id', 'test-id')),
        ('lago_python_client.plans.clients', 'PlanClient', 'find_charge_filter', ('test-id', 'test-id', 'test-id')),
        ('lago_python_client.plans.clients', 'PlanClient', 'create_charge_filter', ('test-id', 'test-id', INPUT)),
        ('lago_python_client.plans.clients', 'PlanClient', 'update_charge_filter', ('test-id', 'test-id', 'test-id', INPUT)),
        ('lago_python_client.plans.clients', 'PlanClient', 'destroy_charge_filter', ('test-id', 'test-id', 'test-id')),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'lifetime_usage', ('test-id',)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'update_lifetime_usage', ('test-id', 1)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'create_alerts', ('test-id', INPUT)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'delete_alerts', ('test-id',)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'find_all_charge_filters', ('test-id', 'test-id')),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'find_charge_filter', ('test-id', 'test-id', 'test-id')),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'create_charge_filter', ('test-id', 'test-id', INPUT)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'update_charge_filter', ('test-id', 'test-id', 'test-id', INPUT)),
        ('lago_python_client.subscriptions.clients', 'SubscriptionClient', 'destroy_charge_filter', ('test-id', 'test-id', 'test-id')),
        ('lago_python_client.usages.clients', 'UsageClient', 'find_all', ()),
        ('lago_python_client.wallets.clients', 'WalletClient', 'replace_metadata', ('test-id', {})),
        ('lago_python_client.wallets.clients', 'WalletClient', 'merge_metadata', ('test-id', {})),
        ('lago_python_client.wallets.clients', 'WalletClient', 'delete_all_metadata', ('test-id',)),
        ('lago_python_client.wallets.clients', 'WalletClient', 'delete_metadata_key', ('test-id', 'test-id')),
        ('lago_python_client.wallets.clients', 'WalletTransactionClient', 'create', (INPUT,)),
        ('lago_python_client.wallets.clients', 'WalletTransactionClient', 'find_all', ('test-id',)),
        ('lago_python_client.wallets.clients', 'WalletTransactionClient', 'payment_url', ('test-id',)),
        ('lago_python_client.wallets.clients', 'WalletTransactionClient', 'consumptions', ('test-id',)),
        ('lago_python_client.wallets.clients', 'WalletTransactionClient', 'fundings', ('test-id',)),
        ('lago_python_client.webhooks.clients', 'WebhookClient', 'public_key', ()),
    ],
)
@pytest.mark.parametrize("policy", [{"retry_on_rate_limit": False}, {"max_retries": 0}, {"max_retries": 1}])
def test_custom_action_rate_limit_policy(
    module, client_class, action, args, policy, httpx_mock: HTTPXMock, monkeypatch
):
    monkeypatch.setattr("lago_python_client.services.rate_limit.time.sleep", lambda _: None)
    client = getattr(import_module(module), client_class)(
        base_url="https://api.getlago.com/api/v1",
        base_ingest_url="https://api.getlago.com/api/v1",
        api_key="test-key",
        rate_limit_retry_config=RateLimitRetryConfig(**policy),
    )
    httpx_mock.add_response(status_code=429, headers={"x-ratelimit-reset": "0"}, is_reusable=True)

    with pytest.raises(LagoRateLimitError):
        getattr(client, action)(*args)

    assert len(httpx_mock.get_requests()) == (2 if policy.get("max_retries") == 1 else 1)
