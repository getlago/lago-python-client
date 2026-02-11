import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import (
    Alert,
    AlertThreshold,
    AlertThresholdList,
)

from .utils.mixin import mock_response


def alert_object():
    threshold = AlertThreshold(code="warn", value=10000)

    return Alert(
        alert_type="wallet_balance_amount",
        code="wallet_balance_alert",
        name="Balance Amount Alert",
        thresholds=AlertThresholdList(__root__=[threshold]),
    )


def test_valid_create_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts",
        content=mock_response("wallet_alert"),
    )
    response = client.customers.wallets.alerts.create("customer_id", "wallet_code", alert_object())

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.lago_organization_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.external_subscription_id is None
    assert response.lago_wallet_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.wallet_code == "wallet_code"
    assert response.code == "wallet_balance_alert"
    assert response.name == "Balance Amount Alert"
    assert response.alert_type == "wallet_balance_amount"
    assert response.direction == "increasing"
    assert response.previous_value == 1000
    assert response.thresholds == AlertThresholdList(
        __root__=[AlertThreshold(code="warn", value=10000, recurring=False)]
    )
    assert response.billable_metric is None


def test_invalid_create_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.alerts.create("customer_id", "wallet_code", alert_object())


def test_valid_update_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        content=mock_response("wallet_alert"),
    )
    response = client.customers.wallets.alerts.update("customer_id", "wallet_code", code, alert_object())

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_update_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.alerts.update("customer_id", "wallet_code", code, alert_object())


def test_valid_find_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        content=mock_response("wallet_alert"),
    )
    response = client.customers.wallets.alerts.find("customer_id", "wallet_code", code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_find_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.alerts.find("customer_id", "wallet_code", code)


def test_valid_destroy_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        content=mock_response("wallet_alert"),
    )
    response = client.customers.wallets.alerts.destroy("customer_id", "wallet_code", code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_destroy_customer_wallet_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.alerts.destroy("customer_id", "wallet_code", code)


def test_valid_find_all_customer_wallet_alerts_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts",
        content=mock_response("wallet_alert_index"),
    )
    response = client.customers.wallets.alerts.find_all("customer_id", "wallet_code")

    assert response["alerts"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_wallet_alerts_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts?page=1&per_page=2",
        content=mock_response("wallet_alert_index"),
    )
    response = client.customers.wallets.alerts.find_all(
        "customer_id", "wallet_code", options={"per_page": 2, "page": 1}
    )

    assert response["alerts"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_wallet_alerts_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/customer_id/wallets/wallet_code/alerts",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customers.wallets.alerts.find_all("customer_id", "wallet_code")
