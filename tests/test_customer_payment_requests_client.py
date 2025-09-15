import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

from .utils.mixin import mock_response


def test_valid_find_all_customer_payment_requests_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_requests",
        content=mock_response(mock="payment_request_index"),
    )
    response = client.customer_payment_requests.find_all(resource_id="external_customer_id")

    assert response["payment_requests"][0].lago_id == "89b6b61e-4dbc-4307-ac96-4abcfa9e3e2d"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_payment_requests_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_requests?per_page=2&page=1",
        content=mock_response(mock="payment_request_index"),
    )
    response = client.customer_payment_requests.find_all(
        resource_id="external_customer_id", options={"per_page": 2, "page": 1}
    )

    assert response["payment_requests"][0].lago_id == "89b6b61e-4dbc-4307-ac96-4abcfa9e3e2d"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_payment_request_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_requests",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customer_payment_requests.find_all(resource_id="external_customer_id")
