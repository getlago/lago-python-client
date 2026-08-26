import os
from urllib.parse import urlencode

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.order import OrderExecute

ENDPOINT = "https://api.getlago.com/api/v1/orders"
ORDER_ID = "cc33cc33-cc33-cc33-cc33-cc33cc33cc33"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_order_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{ORDER_ID}",
        content=mock_response("fixtures/order.json"),
    )
    response = client.orders.find(ORDER_ID)

    assert response.lago_id == ORDER_ID
    assert response.number == "OR-2026-0001"
    assert response.status == "created"
    assert response.order_type == "subscription_creation"
    assert response.execution_mode == "execute_in_lago"
    assert response.executed_at is None
    assert response.execution_record.errors == []
    assert response.lago_order_form_id == "aa11aa11-aa11-aa11-aa11-aa11aa11aa11"
    assert response.billing_snapshot.plans[0].payload["code"] == "premium_plan"


def test_invalid_find_order_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "/invalid",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.orders.find("invalid")


def test_valid_find_all_order_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        content=mock_response("fixtures/order_index.json"),
    )
    response = client.orders.find_all()

    assert response["orders"][0].number == "OR-2026-0001"
    assert response["orders"][1].status == "failed"
    assert response["orders"][1].execution_mode is None
    assert response["orders"][1].execution_record.errors == ["plan_not_found"]
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_order_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    options = {"per_page": 2, "page": 1, "status[]": ["created"], "execution_mode[]": ["execute_in_lago"]}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "?" + urlencode(options, doseq=True),
        content=mock_response("fixtures/order_index.json"),
    )
    response = client.orders.find_all(options)

    assert response["orders"][0].number == "OR-2026-0001"
    assert response["meta"]["current_page"] == 1


def test_valid_execute_order_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_ID}/execute",
        content=mock_response("fixtures/executed_order.json"),
    )
    response = client.orders.execute(ORDER_ID)

    assert response.lago_id == ORDER_ID
    assert response.status == "executed"
    assert response.executed_at == "2026-07-01T00:00:00Z"
    assert response.execution_record.subscription_ids == ["dd44dd44-dd44-dd44-dd44-dd44dd44dd44"]
    assert response.execution_record.applied_coupon_ids == ["ee55ee55-ee55-ee55-ee55-ee55ee55ee55"]


def test_valid_execute_order_request_with_execution_mode(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_ID}/execute",
        match_content=b'{"order":{"execution_mode":"execute_in_lago"}}',
        content=mock_response("fixtures/executed_order.json"),
    )
    response = client.orders.execute(ORDER_ID, OrderExecute(execution_mode="execute_in_lago"))

    assert response.status == "executed"


def test_invalid_execute_order_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_ID}/execute",
        status_code=422,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.orders.execute(ORDER_ID)


def test_execute_order_request_with_missing_catalog_record(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_ID}/execute",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.orders.execute(ORDER_ID)
