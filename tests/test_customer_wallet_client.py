import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import (
    AppliesTo,
    InvoiceCustomSectionInput,
    RecurringTransactionRule,
    RecurringTransactionRuleList,
    Wallet,
)

from .utils.mixin import mock_response


def wallet_object():
    rule = RecurringTransactionRule(
        trigger="interval",
        interval="monthly",
        paid_credits="105.0",
        granted_credits="105.0",
        method="target",
        target_ongoing_balance="105.0",
        transaction_name="Recurring Transaction Rule",
        ignore_paid_top_up_limits=True,
    )
    rules_list = RecurringTransactionRuleList(__root__=[rule])
    applies_to = AppliesTo(
        fee_types=["charge"],
        billable_metric_codes=["usage"],
    )
    return Wallet(
        name="name",
        code="wallet_code",
        priority=30,
        rate_amount="1",
        paid_credits="10",
        granted_credits="10",
        recurring_transaction_rules=rules_list,
        applies_to=applies_to,
        invoice_requires_successful_payment=False,
        transaction_name="Transaction Name",
        paid_top_up_max_amount_cents=10000,
        paid_top_up_min_amount_cents=500,
    )


def test_valid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        content=mock_response("wallet"),
        match_json={
            "wallet": {
                "rate_amount": "1",
                "name": "name",
                "code": "wallet_code",
                "priority": 30,
                "paid_credits": "10",
                "granted_credits": "10",
                "paid_top_up_max_amount_cents": 10000,
                "paid_top_up_min_amount_cents": 500,
                "recurring_transaction_rules": [
                    {
                        "interval": "monthly",
                        "trigger": "interval",
                        "method": "target",
                        "paid_credits": "105.0",
                        "granted_credits": "105.0",
                        "target_ongoing_balance": "105.0",
                        "transaction_name": "Recurring Transaction Rule",
                        "ignore_paid_top_up_limits": True,
                    }
                ],
                "invoice_requires_successful_payment": False,
                "transaction_name": "Transaction Name",
                "applies_to": {"fee_types": ["charge"], "billable_metric_codes": ["usage"]},
            }
        },
    )
    response = client.customers.wallets.create("customer_id", wallet_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.recurring_transaction_rules.__root__[0].lago_id == "12345"
    assert response.recurring_transaction_rules.__root__[0].trigger == "interval"
    assert response.recurring_transaction_rules.__root__[0].interval == "monthly"
    assert response.recurring_transaction_rules.__root__[0].ignore_paid_top_up_limits is True
    assert response.applies_to.fee_types[0] == "charge"
    assert response.applies_to.billable_metric_codes[0] == "usage"
    assert response.paid_top_up_max_amount_cents == 10000
    assert response.paid_top_up_min_amount_cents == 500


def test_invalid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.create("customer_id", wallet_object())


def test_valid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        content=mock_response("wallet"),
    )
    response = client.customers.wallets.update("customer_id", arg, wallet_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.update("customer_id", arg, wallet_object())


def test_valid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        content=mock_response("wallet"),
    )
    response = client.customers.wallets.find("customer_id", arg)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.find("customer_id", arg)


def test_valid_destroy_customer_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        content=mock_response("wallet"),
    )
    response = client.customers.wallets.destroy("customer_id", arg)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_destroy_customer_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + arg,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.destroy("customer_id", arg)


def test_valid_find_all_customer_wallets_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        content=mock_response("wallet_index"),
    )
    response = client.customers.wallets.find_all("customer_id")

    assert response["wallets"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_wallets_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets?per_page=2&page=1",
        content=mock_response("wallet_index"),
    )
    response = client.customers.wallets.find_all("customer_id", options={"per_page": 2, "page": 1})

    assert response["wallets"][1].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.find_all("customer_id")


def test_valid_create_customer_wallet_with_invoice_custom_section(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    invoice_custom_section = InvoiceCustomSectionInput(
        skip_invoice_custom_sections=False,
        invoice_custom_section_codes=["section_code_1"],
    )

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        content=mock_response("wallet"),
    )
    wallet = wallet_object()
    wallet.invoice_custom_section = invoice_custom_section
    response = client.customers.wallets.create("customer_id", wallet)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.applied_invoice_custom_sections.__root__[0].lago_id == "ics_wallet_001"
    assert response.applied_invoice_custom_sections.__root__[0].invoice_custom_section_id == "section_wallet_001"
    assert response.applied_invoice_custom_sections.__root__[0].created_at == "2022-04-29T08:59:51Z"


def test_valid_update_customer_wallet_with_invoice_custom_section(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    invoice_custom_section = InvoiceCustomSectionInput(
        skip_invoice_custom_sections=False,
        invoice_custom_section_codes=["section_code_1"],
    )

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + wallet_id,
        content=mock_response("wallet"),
    )
    wallet = wallet_object()
    wallet.invoice_custom_section = invoice_custom_section
    response = client.customers.wallets.update("customer_id", wallet_id, wallet)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.applied_invoice_custom_sections.__root__[0].lago_id == "ics_wallet_001"
    assert response.applied_invoice_custom_sections.__root__[0].invoice_custom_section_id == "section_wallet_001"


def test_valid_create_customer_wallet_with_invoice_custom_section_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets",
        content=mock_response("wallet"),
    )
    response = client.customers.wallets.create("customer_id", wallet_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert (
        response.recurring_transaction_rules.__root__[0].applied_invoice_custom_sections.__root__[0].lago_id
        == "ics_rule_001"
    )
    assert (
        response.recurring_transaction_rules.__root__[0]
        .applied_invoice_custom_sections.__root__[0]
        .invoice_custom_section_id
        == "section_rule_001"
    )


def test_valid_update_customer_wallet_with_invoice_custom_section_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    invoice_custom_section = InvoiceCustomSectionInput(
        skip_invoice_custom_sections=False,
        invoice_custom_section_codes=["section_code_1"],
    )
    rule = RecurringTransactionRule(
        trigger="interval",
        interval="monthly",
        paid_credits="105.0",
        granted_credits="105.0",
        invoice_custom_section=invoice_custom_section,
    )
    rules_list = RecurringTransactionRuleList(__root__=[rule])

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/" + wallet_id,
        content=mock_response("wallet"),
    )
    wallet = Wallet(name="name", recurring_transaction_rules=rules_list)
    response = client.customers.wallets.update("customer_id", wallet_id, wallet)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert (
        response.recurring_transaction_rules.__root__[0].applied_invoice_custom_sections.__root__[0].lago_id
        == "ics_rule_001"
    )
