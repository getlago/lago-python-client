import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import (
    AppliesTo,
    RecurringTransactionRule,
    RecurringTransactionRuleList,
    PaymentMethod,
    Wallet,
)


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
        external_customer_id="12345",
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


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/wallet.json")

    with open(data_path, "rb") as wallet_response:
        return wallet_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/wallet_index.json")

    with open(data_path, "rb") as wallet_response:
        return wallet_response.read()


def test_valid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        content=mock_response(),
        match_json={
            "wallet": {
                "external_customer_id": "12345",
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
    response = client.wallets.create(wallet_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.recurring_transaction_rules.__root__[0].lago_id == "12345"
    assert response.recurring_transaction_rules.__root__[0].trigger == "interval"
    assert response.recurring_transaction_rules.__root__[0].interval == "monthly"
    assert response.recurring_transaction_rules.__root__[0].ignore_paid_top_up_limits is True
    assert response.applies_to.fee_types[0] == "charge"
    assert response.applies_to.billable_metric_codes[0] == "usage"
    assert response.paid_top_up_max_amount_cents == 10000
    assert response.paid_top_up_min_amount_cents == 500


def test_valid_create_wallet_request_with_payment_method_on_wallet(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    payment_method = PaymentMethod(payment_method_type="card", payment_method_id="pm_123")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        content=mock_response(),
    )
    wallet = wallet_object()
    wallet.payment_method = payment_method
    response = client.wallets.create(wallet)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.payment_method.payment_method_type == "card"
    assert response.payment_method.payment_method_id == "pm_123"


def test_invalid_create_wallet_request_with_payment_method_on_wallet(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    payment_method = PaymentMethod(payment_method_type="provider", payment_method_id="invalid-id")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        status_code=422,
        json={
            "status": 422,
            "error": "Unprocessable Entity",
            "code": "validation_errors",
            "error_details": {"payment_method": ["invalid_payment_method"]},
        },
    )

    wallet = wallet_object()
    wallet.payment_method = payment_method

    with pytest.raises(LagoApiError):
        client.wallets.create(wallet)


def test_valid_create_wallet_request_with_payment_method_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        content=mock_response(),
    )
    response = client.wallets.create(wallet_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.recurring_transaction_rules.__root__[0].payment_method.payment_method_type == "card"
    assert response.recurring_transaction_rules.__root__[0].payment_method.payment_method_id == "pm_123"


def test_invalid_create_wallet_request_with_payment_method_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    payment_method = PaymentMethod(payment_method_type="provider", payment_method_id="invalid-id")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        status_code=422,
        json={
            "status": 422,
            "error": "Unprocessable Entity",
            "code": "validation_errors",
            "error_details": {"payment_method": ["invalid_payment_method"]},
        },
    )

    wallet = wallet_object()
    wallet.recurring_transaction_rules.__root__[0].payment_method = payment_method

    with pytest.raises(LagoApiError):
        client.wallets.create(wallet)


def test_invalid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallets.create(wallet_object())


def test_valid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        content=mock_response(),
    )
    response = client.wallets.update(wallet_object(), wallet_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_valid_update_wallet_request_with_payment_method_on_wallet(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    payment_method = PaymentMethod(payment_method_type="card", payment_method_id="pm_123")

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        content=mock_response(),
    )
    wallet = wallet_object()
    wallet.payment_method = payment_method
    response = client.wallets.update(wallet, wallet_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.payment_method.payment_method_type == "card"
    assert response.payment_method.payment_method_id == "pm_123"


def test_invalid_update_wallet_request_with_payment_method_on_wallet(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    payment_method = PaymentMethod(payment_method_type="provider", payment_method_id="invalid-id")

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        status_code=422,
        json={
            "status": 422,
            "error": "Unprocessable Entity",
            "code": "validation_errors",
            "error_details": {"payment_method": ["invalid_payment_method"]},
        },
    )

    wallet = wallet_object()
    wallet.payment_method = payment_method

    with pytest.raises(LagoApiError):
        client.wallets.update(wallet, wallet_id)


def test_valid_update_wallet_request_with_payment_method_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        content=mock_response(),
    )
    response = client.wallets.update(wallet_object(), wallet_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.recurring_transaction_rules.__root__[0].payment_method.payment_method_type == "card"
    assert response.recurring_transaction_rules.__root__[0].payment_method.payment_method_id == "pm_123"


def test_invalid_update_wallet_request_with_payment_method_on_recurring_transaction_rule(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    payment_method = PaymentMethod(payment_method_type="provider", payment_method_id="invalid-id")

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        status_code=422,
        json={
            "status": 422,
            "error": "Unprocessable Entity",
            "code": "validation_errors",
            "error_details": {"payment_method": ["invalid_payment_method"]},
        },
    )

    wallet = wallet_object()
    wallet.recurring_transaction_rules.__root__[0].payment_method = payment_method

    with pytest.raises(LagoApiError):
        client.wallets.update(wallet, wallet_id)


def test_invalid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    wallet_id = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallets.update(wallet_object(), wallet_id)


def test_valid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        content=mock_response(),
    )
    response = client.wallets.find(wallet_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    wallet_id = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallets.find(wallet_id)


def test_valid_destroy_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        content=mock_response(),
    )
    response = client.wallets.destroy(wallet_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_destroy_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    wallet_id = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallets.destroy(wallet_id)


def test_valid_find_all_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets",
        content=mock_collection_response(),
    )
    response = client.wallets.find_all()

    assert response["wallets"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_wallet_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets?external_customer_id=123&per_page=2&page=1",
        content=mock_collection_response(),
    )
    response = client.wallets.find_all({"external_customer_id": 123, "per_page": 2, "page": 1})

    assert response["wallets"][1].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallets.find_all()


def mock_metadata_response():
    return b'{"metadata": {"foo": "bar", "baz": null}}'


def mock_null_metadata_response():
    return b'{"metadata": null}'


def test_valid_replace_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.wallets.replace_metadata(wallet_id, {"foo": "bar", "baz": None})

    assert response == {"foo": "bar", "baz": None}


def test_valid_merge_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PATCH",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.wallets.merge_metadata(wallet_id, {"foo": "qux"})

    assert response == {"foo": "bar", "baz": None}


def test_valid_delete_all_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id + "/metadata",
        content=mock_null_metadata_response(),
    )
    response = client.wallets.delete_all_metadata(wallet_id)

    assert response is None


def test_valid_delete_metadata_key_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    wallet_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    key = "foo"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/wallets/" + wallet_id + "/metadata/" + key,
        content=b'{"metadata": {"baz": "qux"}}',
    )
    response = client.wallets.delete_metadata_key(wallet_id, key)

    assert response == {"baz": "qux"}
