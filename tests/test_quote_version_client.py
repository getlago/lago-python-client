import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.quote import QuoteVersionApprove

ENDPOINT = "https://api.getlago.com/api/v1/quote_versions"
QUOTE_VERSION_ID = "4d234d23-4d23-4d23-4d23-4d234d234d23"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}",
        content=mock_response("fixtures/quote_version.json"),
    )
    response = client.quote_versions.find(QUOTE_VERSION_ID)

    assert response.lago_id == QUOTE_VERSION_ID
    assert response.version == 1
    assert response.status == "draft"
    assert response.void_reason is None
    assert response.billing_entity_code == "acme_corp"
    assert "QT-2026-0001" in response.content
    assert response.billing_items.plans[0].payload["code"] == "premium_plan"
    assert response.billing_items.plans[0].overrides["amountCents"] == 50000
    assert response.billing_items.coupons[0].type == "coupon"
    assert response.billing_items.walletCredits[0].payload["paidCredits"] == "100.0"
    assert response.billing_items.addOns is None


def test_invalid_find_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "/invalid",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.quote_versions.find("invalid")


def test_valid_approve_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}/approve",
        content=mock_response("fixtures/quote_version.json"),
    )
    response = client.quote_versions.approve(QUOTE_VERSION_ID)

    assert response.lago_id == QUOTE_VERSION_ID


def test_valid_approve_quote_version_request_with_expires_at(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}/approve",
        match_content=b'{"expires_at":"2026-06-30T23:59:59Z"}',
        content=mock_response("fixtures/quote_version.json"),
    )
    response = client.quote_versions.approve(
        QUOTE_VERSION_ID,
        QuoteVersionApprove(expires_at="2026-06-30T23:59:59Z"),
    )

    assert response.lago_id == QUOTE_VERSION_ID


def test_invalid_approve_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}/approve",
        status_code=422,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.quote_versions.approve(QUOTE_VERSION_ID)


def test_valid_void_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}/void",
        content=mock_response("fixtures/quote_version.json"),
    )
    response = client.quote_versions.void(QUOTE_VERSION_ID)

    assert response.lago_id == QUOTE_VERSION_ID


def test_valid_clone_quote_version_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{QUOTE_VERSION_ID}/clone",
        content=mock_response("fixtures/quote_version.json"),
    )
    response = client.quote_versions.clone(QUOTE_VERSION_ID)

    assert response.lago_id == QUOTE_VERSION_ID
