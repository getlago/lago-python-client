import os
from urllib.parse import urlencode

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

ENDPOINT = "https://api.getlago.com/api/v1/api_logs"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_api_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    request_id = "8fae2f0e-fe8e-44d3-bbf7-1c552eba3a24"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{request_id}",
        content=mock_response("fixtures/api_log.json"),
    )
    response = client.api_logs.find(request_id)

    assert response.request_id == request_id
    assert response.client == "LagoClient.0.0.0"


def test_invalid_find_api_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    request_id = "invalid"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{request_id}",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.api_logs.find(request_id)


def test_valid_find_all_api_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        content=mock_response("fixtures/api_log_index.json"),
    )
    response = client.api_logs.find_all()

    assert response["api_logs"][0].request_id == "8fae2f0e-fe8e-44d3-bbf7-1c552eba3a24"
    assert response["api_logs"][1].request_id == "65ec835e-43f4-40ad-a4bd-da663349d583"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_api_log_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    options = {"per_page": 1, "page": 1}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"?{urlencode(options)}",
        content=mock_response("fixtures/api_log_index.json"),
    )
    response = client.api_logs.find_all(options)

    assert response["api_logs"][1].request_id == "65ec835e-43f4-40ad-a4bd-da663349d583"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_api_log_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.api_logs.find_all()


def test_invalid_operations_for_api_log_request():
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    assert not hasattr(client.api_logs, "create")
    assert not hasattr(client.api_logs, "update")
    assert not hasattr(client.api_logs, "destroy")
