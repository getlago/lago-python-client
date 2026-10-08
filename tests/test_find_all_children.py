import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


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
