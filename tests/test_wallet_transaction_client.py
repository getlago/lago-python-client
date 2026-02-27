import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import PaymentMethod, WalletTransaction


def wallet_transaction_object():
    return WalletTransaction(
        wallet_id="123",
        paid_credits="10",
        granted_credits="10",
        voided_credits="0",
        name="Transaction Name",
        invoice_requires_successful_payment=False,
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/wallet_transaction.json")

    with open(data_path, "rb") as wallet_transaction_response:
        return wallet_transaction_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "fixtures/wallet_transaction_index.json")

    with open(data_path, "rb") as wallet_transaction_index_response:
        return wallet_transaction_index_response.read()


def mock_payment_url_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/wallet_transaction_payment_url.json")

    with open(data_path, "rb") as payment_url_response:
        return payment_url_response.read()


def test_valid_create_wallet_transaction_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallet_transactions",
        content=mock_response(),
    )
    response = client.wallet_transactions.create(wallet_transaction_object())

    assert response["wallet_transactions"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["wallet_transactions"][1].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1222"
    assert response["wallet_transactions"][2].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1333"
    assert response["wallet_transactions"][0].status == "settled"
    assert response["wallet_transactions"][2].status == "failed"
    assert response["wallet_transactions"][2].failed_at == "2022-04-29T08:59:51Z"
    assert response["wallet_transactions"][0].name == "Transaction Name"
    assert response["wallet_transactions"][1].name == "Transaction Name"
    assert response["wallet_transactions"][2].name == "Transaction Name"


def test_valid_create_wallet_transaction_request_with_payment_method(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    payment_method = PaymentMethod(payment_method_type="card", payment_method_id="pm_123")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallet_transactions",
        content=mock_response(),
    )
    transaction = wallet_transaction_object()
    transaction.payment_method = payment_method
    response = client.wallet_transactions.create(transaction)

    assert response["wallet_transactions"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["wallet_transactions"][0].status == "settled"
    assert response["wallet_transactions"][0].payment_method.payment_method_type == "card"
    assert response["wallet_transactions"][0].payment_method.payment_method_id == "pm_123"
    assert response["wallet_transactions"][1].payment_method.payment_method_type == "card"
    assert response["wallet_transactions"][1].payment_method.payment_method_id == "pm_123"
    assert response["wallet_transactions"][2].payment_method.payment_method_type == "card"
    assert response["wallet_transactions"][2].payment_method.payment_method_id == "pm_123"


def test_invalid_create_wallet_transaction_request_with_payment_method(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    payment_method = PaymentMethod(payment_method_type="provider", payment_method_id="invalid-id")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallet_transactions",
        status_code=422,
        json={
            "status": 422,
            "error": "Unprocessable Entity",
            "code": "validation_errors",
            "error_details": {"payment_method": ["invalid_payment_method"]},
        },
    )

    transaction = wallet_transaction_object()
    transaction.payment_method = payment_method

    with pytest.raises(LagoApiError):
        client.wallet_transactions.create(transaction)


def test_invalid_create_wallet_transaction_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallet_transactions",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.wallet_transactions.create(wallet_transaction_object())


def test_valid_find_all_wallet_transactions_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/wallets/555/wallet_transactions",
        content=mock_collection_response(),
    )
    response = client.wallet_transactions.find_all("555")

    assert response["wallet_transactions"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["meta"]["current_page"] == 1


def test_valid_payment_url_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/wallet_transactions/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/payment_url",
        content=mock_payment_url_response(),
    )
    response = client.wallet_transactions.payment_url("5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba")

    assert response == "https://checkout.stripe.com/c/pay/cs_test_a1cuqFkXvH"
