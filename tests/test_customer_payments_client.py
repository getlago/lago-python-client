import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

from .utils.mixin import mock_response


def test_valid_find_all_customer_payments_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payments",
        content=mock_response(mock="payment_index"),
    )
    response = client.customer_payments.find_all(resource_id="external_customer_id")

    assert response["payments"][0].lago_id == "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_payments_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payments?per_page=2&page=1",
        content=mock_response(mock="payment_index"),
    )
    response = client.customer_payments.find_all(resource_id="external_customer_id", options={"per_page": 2, "page": 1})

    assert response["payments"][0].lago_id == "8e5d5ec2-bdc7-4c43-a944-5ababae775d4"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_payment_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payments",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customer_payments.find_all(resource_id="external_customer_id")
