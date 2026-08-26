import os
from urllib.parse import urlencode

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.order_form import OrderFormMarkAsSigned

ENDPOINT = "https://api.getlago.com/api/v1/order_forms"
ORDER_FORM_ID = "aa11aa11-aa11-aa11-aa11-aa11aa11aa11"


def mock_response(fixture_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, fixture_path)

    with open(data_path, "rb") as response:
        return response.read()


def test_valid_find_order_form_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + f"/{ORDER_FORM_ID}",
        content=mock_response("fixtures/order_form.json"),
    )
    response = client.order_forms.find(ORDER_FORM_ID)

    assert response.lago_id == ORDER_FORM_ID
    assert response.number == "OF-2026-0001"
    assert response.status == "generated"
    assert response.void_reason is None
    assert response.signed_document_url is None
    assert response.lago_quote_version_id == "4d234d23-4d23-4d23-4d23-4d234d234d23"


def test_invalid_find_order_form_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "/invalid",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.order_forms.find("invalid")


def test_valid_find_all_order_form_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT,
        content=mock_response("fixtures/order_form_index.json"),
    )
    response = client.order_forms.find_all()

    assert response["order_forms"][0].number == "OF-2026-0001"
    assert response["order_forms"][1].status == "voided"
    assert response["order_forms"][1].void_reason == "manual"
    assert response["order_forms"][1].expires_at is None
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_order_form_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    options = {"per_page": 2, "page": 1, "status[]": ["generated"], "search_term": "OF-2026"}

    httpx_mock.add_response(
        method="GET",
        url=ENDPOINT + "?" + urlencode(options, doseq=True),
        content=mock_response("fixtures/order_form_index.json"),
    )
    response = client.order_forms.find_all(options)

    assert response["order_forms"][0].number == "OF-2026-0001"
    assert response["meta"]["current_page"] == 1


def test_valid_mark_as_signed_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_FORM_ID}/mark_as_signed",
        content=mock_response("fixtures/signed_order_form.json"),
    )
    response = client.order_forms.mark_as_signed(ORDER_FORM_ID)

    assert response.lago_id == ORDER_FORM_ID
    assert response.status == "signed"


def test_valid_mark_as_signed_request_with_params(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_FORM_ID}/mark_as_signed",
        match_content=(b'{"order_form":{"execution_mode":"execute_in_lago","execute_at":"2026-07-01T00:00:00Z"}}'),
        content=mock_response("fixtures/signed_order_form.json"),
    )
    response = client.order_forms.mark_as_signed(
        ORDER_FORM_ID,
        OrderFormMarkAsSigned(
            execution_mode="execute_in_lago",
            execute_at="2026-07-01T00:00:00Z",
        ),
    )

    assert response.status == "signed"
    assert response.signed_at == "2026-05-02T10:15:00Z"
    assert "OF-2026-0001" in response.signed_document_url


def test_invalid_mark_as_signed_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_FORM_ID}/mark_as_signed",
        status_code=422,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.order_forms.mark_as_signed(ORDER_FORM_ID)


def test_valid_void_order_form_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_FORM_ID}/void",
        content=mock_response("fixtures/order_form.json"),
    )
    response = client.order_forms.void(ORDER_FORM_ID)

    assert response.lago_id == ORDER_FORM_ID


def test_invalid_void_order_form_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url=ENDPOINT + f"/{ORDER_FORM_ID}/void",
        status_code=422,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.order_forms.void(ORDER_FORM_ID)
