import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Payment


def payment_object():
    return Payment(
        amount_cents=100,
        reference="ref1",
        invoice_id="f8e194df-5d90-4382-b146-c881d2c67f28",
        paid_at="2025-01-01T13:00:00Z",
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/payment.json")

    with open(data_path, "rb") as payment_response:
        return payment_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "fixtures/payment_index.json")

    with open(data_path, "rb") as payments_response:
        return payments_response.read()


def assert_new_payment_fields(response):
    assert response.status == "succeeded"
    assert response.lago_customer_id == "99a6094e-199b-4101-896a-54e927ce7bd7"
    assert response.external_customer_id == "customer_external_id"
    assert response.lago_payable_id == "f8e194df-5d90-4382-b146-c881d2c67f28"
    assert response.payable_type == "Invoice"
    assert response.payment_provider_code == "stripe_prod"
    assert response.payment_provider_type == "stripe"
    assert response.provider_payment_id == "pi_123"
    assert response.provider_customer_id == "cus_123"
    assert isinstance(response.next_action, dict)
    assert response.next_action["type"] == "redirect_to_url"
    assert response.next_action["redirect_to_url"]["url"] == "https://example.com"


def test_valid_find_payment_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    identifier = "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payments/" + identifier,
        content=mock_response(),
    )
    response = client.payments.find(identifier)

    assert response.lago_id == identifier
    assert_new_payment_fields(response)


def test_valid_find_all_payments_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payments",
        content=mock_collection_response(),
    )
    response = client.payments.find_all()

    assert response["payments"][0].lago_id == "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"
    assert response["payments"][0].payment_provider_type == "stripe"
    assert response["payments"][0].next_action["type"] == "redirect_to_url"
    assert response["payments"][1].status == "succeeded"
    assert response["payments"][1].payable_type == "Invoice"
    assert response["payments"][1].payment_provider_code is None
    assert response["payments"][1].payment_provider_type is None
    assert response["payments"][1].provider_payment_id is None
    assert response["payments"][1].provider_customer_id is None
    assert response["payments"][1].next_action == {}
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_payments_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payments?per_page=2&page=1",
        content=mock_collection_response(),
    )
    response = client.payments.find_all({"per_page": 2, "page": 1})

    assert response["payments"][0].lago_id == "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_payment_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payments",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.payments.find_all()


def test_valid_create_payment_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/payments",
        content=mock_response(),
    )
    response = client.payments.create(payment_object())

    assert response is not None
    assert response.lago_id == "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"
    assert response.amount_cents == 100
    assert response.amount_currency == "USD"
    assert response.payment_status == "succeeded"
    assert len(response.invoice_ids) == 1
    assert response.invoice_ids[0] == "f8e194df-5d90-4382-b146-c881d2c67f28"
    assert len(response.invoice_numbers) == 1
    assert response.invoice_numbers[0] == "LAG-1234-567-890"
    assert_new_payment_fields(response)


def test_invalid_create_payment_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/payments",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.payments.create(payment_object())
