import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

from .utils.mixin import mock_response


def test_valid_find_all_customer_payment_methods_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods",
        content=mock_response(mock="payment_method_index"),
    )
    response = client.customer_payment_methods.find_all(resource_id="external_customer_id")

    assert response["payment_methods"][0].lago_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    assert response["payment_methods"][0].is_default is True
    assert response["payment_methods"][0].payment_provider_code == "stripe_1"
    assert response["payment_methods"][0].payment_provider_name == "Stripe"
    assert response["payment_methods"][0].payment_provider_type == "stripe"
    assert response["payment_methods"][0].provider_method_id == "pm_1234567890"
    assert response["payment_methods"][0].created_at == "2024-01-01T00:00:00Z"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_payment_methods_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods?per_page=2&page=1",
        content=mock_response(mock="payment_method_index"),
    )
    response = client.customer_payment_methods.find_all(
        resource_id="external_customer_id", options={"per_page": 2, "page": 1}
    )

    assert response["payment_methods"][0].lago_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    assert response["payment_methods"][0].is_default is True
    assert response["payment_methods"][0].payment_provider_code == "stripe_1"
    assert response["payment_methods"][0].payment_provider_name == "Stripe"
    assert response["payment_methods"][0].payment_provider_type == "stripe"
    assert response["payment_methods"][0].provider_method_id == "pm_1234567890"
    assert response["payment_methods"][0].created_at == "2024-01-01T00:00:00Z"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_customer_payment_methods_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/invalid_customer_id/payment_methods",
        status_code=404,
        content=b'{"status": 404, "error": "Not Found", "code": "customer_not_found"}',
    )

    with pytest.raises(LagoApiError) as exc_info:
        client.customer_payment_methods.find_all(resource_id="invalid_customer_id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.response["code"] == "customer_not_found"


def test_valid_destroy_customer_payment_method_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods/a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        content=mock_response(mock="payment_method"),
    )
    response = client.customer_payment_methods.destroy("external_customer_id", "a1b2c3d4-e5f6-7890-abcd-ef1234567890")

    assert response.lago_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    assert response.is_default is True
    assert response.payment_provider_code == "stripe_1"
    assert response.payment_provider_name == "Stripe"
    assert response.payment_provider_type == "stripe"
    assert response.provider_method_id == "pm_1234567890"
    assert response.created_at == "2024-01-01T00:00:00Z"


def test_invalid_destroy_customer_payment_method_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods/invalid_id",
        status_code=404,
        content=b'{"status": 404, "error": "Not Found", "code": "payment_method_not_found"}',
    )

    with pytest.raises(LagoApiError) as exc_info:
        client.customer_payment_methods.destroy("external_customer_id", "invalid_id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.response["code"] == "payment_method_not_found"


def test_valid_set_as_default_customer_payment_method_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods/a1b2c3d4-e5f6-7890-abcd-ef1234567890/set_as_default",
        content=mock_response(mock="payment_method"),
    )
    response = client.customer_payment_methods.set_as_default(
        "external_customer_id", "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    )

    assert response.lago_id == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    assert response.is_default is True
    assert response.payment_provider_code == "stripe_1"
    assert response.payment_provider_name == "Stripe"
    assert response.payment_provider_type == "stripe"
    assert response.provider_method_id == "pm_1234567890"
    assert response.created_at == "2024-01-01T00:00:00Z"


def test_invalid_set_as_default_customer_payment_method_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/payment_methods/invalid_id/set_as_default",
        status_code=404,
        content=b'{"status": 404, "error": "Not Found", "code": "payment_method_not_found"}',
    )

    with pytest.raises(LagoApiError) as exc_info:
        client.customer_payment_methods.set_as_default("external_customer_id", "invalid_id")

    assert exc_info.value.status_code == 404
    assert exc_info.value.response["code"] == "payment_method_not_found"
