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
        alert_type="billable_metric_current_usage_amount",
        code="storage_threshold_alert",
        name="Storage Usage Alert",
        billable_metric_cod="storage",
        thresholds=AlertThresholdList(__root__=[threshold]),
    )


def test_valid_create_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts",
        content=mock_response("subscription_alert"),
    )
    response = client.subscriptions.alerts.create("subscription_id", alert_object())

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.lago_organization_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.external_subscription_id == "subscription_id"
    assert response.lago_wallet_id is None
    assert response.wallet_code is None
    assert response.code == "storage_threshold_alert"
    assert response.name == "Storage Usage Alert"
    assert response.alert_type == "billable_metric_current_usage_amount"
    assert response.previous_value == 1000
    assert response.billable_metric.code == "storage"
    assert response.thresholds == AlertThresholdList(
        __root__=[AlertThreshold(code="warn", value=99.0, recurring=False)]
    )


def test_invalid_create_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.alerts.create("subscription_id", alert_object())


def test_valid_update_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        content=mock_response("subscription_alert"),
    )
    response = client.subscriptions.alerts.update("subscription_id", code, alert_object())

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_update_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.alerts.update("subscription_id", code, alert_object())


def test_valid_find_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        content=mock_response("subscription_alert"),
    )
    response = client.subscriptions.alerts.find("subscription_id", code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_find_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.alerts.find("subscription_id", code)


def test_valid_destroy_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "alert-code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        content=mock_response("subscription_alert"),
    )
    response = client.subscriptions.alerts.destroy("subscription_id", code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"


def test_invalid_destroy_subscription_alert_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.alerts.destroy("subscription_id", code)


def test_valid_find_all_subscription_alerts_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts",
        content=mock_response("subscription_alert_index"),
    )
    response = client.subscriptions.alerts.find_all("subscription_id")

    assert response["alerts"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_subscription_alerts_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts?page=1&per_page=2",
        content=mock_response("subscription_alert_index"),
    )
    response = client.subscriptions.alerts.find_all("subscription_id", options={"per_page": 2, "page": 1})

    assert response["alerts"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_subscription_alerts_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/subscription_id/alerts",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.alerts.find_all("subscription_id")
