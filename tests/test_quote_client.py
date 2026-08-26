import os
from urllib.parse import urlencode

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

ENDPOINT = "https://api.getlago.com/api/v1/quotes"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_quote_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    quote_id = "1a901a90-1a90-1a90-1a90-1a901a901a90"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{quote_id}",
        content=mock_response("fixtures/quote.json"),
    )
    response = client.quotes.find(quote_id)

    assert response.lago_id == quote_id
    assert response.number == "QT-2026-0001"
    assert response.order_type == "subscription_creation"
    assert response.lago_subscription_id is None
    assert response.current_version.version == 1
    assert response.current_version.status == "draft"
    assert response.owners[0].email == "sales@getlago.com"


def test_invalid_find_quote_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    quote_id = "invalid"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{quote_id}",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.quotes.find(quote_id)


def test_valid_find_all_quote_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        content=mock_response("fixtures/quote_index.json"),
    )
    response = client.quotes.find_all()

    assert response["quotes"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["quotes"][1].order_type == "one_off"
    assert response["quotes"][1].current_version is None
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_quote_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    options = {"per_page": 2, "page": 1, "status[]": ["draft", "approved"]}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "?" + urlencode(options, doseq=True),
        content=mock_response("fixtures/quote_index.json"),
    )
    response = client.quotes.find_all(options)

    assert response["quotes"][0].number == "QT-2026-0001"
    assert response["meta"]["current_page"] == 1


def test_valid_quote_versions_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    quote_id = "1a901a90-1a90-1a90-1a90-1a901a901a90"

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{quote_id}/versions",
        content=mock_response("fixtures/quote_version_index.json"),
    )
    response = client.quotes.versions(quote_id)

    assert response["quote_versions"][0].version == 2
    assert response["quote_versions"][0].status == "draft"
    assert response["quote_versions"][1].status == "voided"
    assert response["quote_versions"][1].void_reason == "superseded"
    assert response["meta"]["current_page"] == 1


def test_valid_quote_versions_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    quote_id = "1a901a90-1a90-1a90-1a90-1a901a901a90"
    options = {"per_page": 2, "page": 1}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{quote_id}/versions?" + urlencode(options),
        content=mock_response("fixtures/quote_version_index.json"),
    )
    response = client.quotes.versions(quote_id, options)

    assert response["quote_versions"][0].version == 2
    assert response["meta"]["current_page"] == 1
