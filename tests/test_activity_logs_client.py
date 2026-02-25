import os
from urllib.parse import urlencode

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

ENDPOINT = "https://api.getlago.com/api/v1/activity_logs"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_activity_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    activity_id = "1262046f-ea6e-423b-8bf7-3a985232f91b"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{activity_id}",
        content=mock_response("fixtures/activity_log.json"),
    )
    response = client.activity_logs.find(activity_id)

    assert response.activity_id == activity_id
    assert response.activity_type == "billable_metric.created"


def test_invalid_find_activity_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    activity_id = "invalid"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{activity_id}",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.activity_logs.find(activity_id)


def test_valid_find_all_activity_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        content=mock_response("fixtures/activity_log_index.json"),
    )
    response = client.activity_logs.find_all()

    assert response["activity_logs"][0].activity_id == "1262046f-ea6e-423b-8bf7-3a985232f91b"
    assert response["activity_logs"][1].activity_id == "6744ddec-3516-4e26-9c7e-dc3c30fc4e80"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_activity_log_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    options = {"per_page": 1, "page": 1}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"?{urlencode(options)}",
        content=mock_response("fixtures/activity_log_index.json"),
    )
    response = client.activity_logs.find_all(options)

    assert response["activity_logs"][1].activity_id == "6744ddec-3516-4e26-9c7e-dc3c30fc4e80"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_activity_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.activity_logs.find_all()


def test_invalid_operations_for_activity_log_request():
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    assert not hasattr(client.activity_logs, "create")
    assert not hasattr(client.activity_logs, "update")
    assert not hasattr(client.activity_logs, "destroy")
