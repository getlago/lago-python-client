import httpx
import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.mixins import DEFAULT_TIMEOUT


@pytest.mark.parametrize(
    "client_name,parent_resource,child_resource",
    [
        ("customer_applied_coupons", "customers", "applied_coupons"),
        ("customer_credit_notes", "customers", "credit_notes"),
        ("customer_invoices", "customers", "invoices"),
        ("customer_payment_methods", "customers", "payment_methods"),
        ("customer_payment_requests", "customers", "payment_requests"),
        ("customer_payments", "customers", "payments"),
        ("customer_subscriptions", "customers", "subscriptions"),
        ("customer_wallets", "customers", "wallets"),
        ("plan_charges", "plans", "charges"),
        ("plan_fixed_charges", "plans", "fixed_charges"),
        ("subscription_charges", "subscriptions", "charges"),
        ("subscription_fixed_charges", "subscriptions", "fixed_charges"),
    ],
)
def test_find_all_children_sends_authentication_headers(
    httpx_mock: HTTPXMock, client_name: str, parent_resource: str, child_resource: str
):
    client = Client(api_key="test-api-key")
    response_data = {child_resource: [], "meta": {"current_page": 1}}
    httpx_mock.add_response(
        method="GET",
        url=f"https://api.getlago.com/api/v1/{parent_resource}/parent-id/{child_resource}?per_page=2&page=1",
        json=response_data,
    )

    response = getattr(client, client_name).find_all(resource_id="parent-id", options={"per_page": 2, "page": 1})

    request = httpx_mock.get_request()
    assert request.headers["Authorization"] == "Bearer test-api-key"
    assert request.headers["Content-Type"] == "application/json"
    assert response == response_data


def mock_invoices_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/parent-id/invoices",
        json={"invoices": [], "meta": {"current_page": 1}},
    )


def test_find_all_children_uses_default_timeout(httpx_mock: HTTPXMock):
    client = Client(api_key="test-api-key")
    mock_invoices_response(httpx_mock)

    client.customer_invoices.find_all(resource_id="parent-id")

    assert httpx_mock.get_request().extensions["timeout"] == DEFAULT_TIMEOUT.as_dict()


def test_find_all_children_with_custom_timeout(httpx_mock: HTTPXMock):
    client = Client(api_key="test-api-key")
    mock_invoices_response(httpx_mock)

    client.customer_invoices.find_all(resource_id="parent-id", timeout=httpx.Timeout(30.0))

    assert httpx_mock.get_request().extensions["timeout"] == httpx.Timeout(30.0).as_dict()


def test_find_all_children_with_deprecated_timetour(httpx_mock: HTTPXMock):
    client = Client(api_key="test-api-key")
    mock_invoices_response(httpx_mock)

    with pytest.warns(DeprecationWarning, match="timetour is deprecated"):
        client.customer_invoices.find_all(resource_id="parent-id", timetour=httpx.Timeout(30.0))

    assert httpx_mock.get_request().extensions["timeout"] == httpx.Timeout(30.0).as_dict()
