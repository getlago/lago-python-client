import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import PaymentRequest

def payment_request_object():
    return PaymentRequest(
        email="gavin@overdue.test",
        external_customer_id="gavin_001",
        lago_invoice_ids=[
            "f8e194df-5d90-4382-b146-c881d2c67f28",
            "a20b1805-d54c-4e57-873d-721cc153035e"
        ],
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/payment_request.json")

    with open(data_path, "rb") as payment_request_response:
        return payment_request_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "fixtures/payment_request_index.json")

    with open(data_path, "rb") as payment_requests_response:
        return payment_requests_response.read()


def test_valid_find_all_payment_requests_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payment_requests",
        content=mock_collection_response(),
    )
    response = client.payment_requests.find_all()

    assert response["payment_requests"][0].lago_id == "89b6b61e-4dbc-4307-ac96-4abcfa9e3e2d"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_payment_requests_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payment_requests?per_page=2&page=1",
        content=mock_collection_response(),
    )
    response = client.payment_requests.find_all({"per_page": 2, "page": 1})

    assert response["payment_requests"][0].lago_id == "89b6b61e-4dbc-4307-ac96-4abcfa9e3e2d"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_payment_requests_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/payment_requests",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.payment_requests.find_all()

def test_valid_create_payment_request_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/payment_requests",
        content=mock_response(),
    )
    response = client.payment_requests.create(payment_request_object())

    assert response.lago_id == "89b6b61e-4dbc-4307-ac96-4abcfa9e3e2d"
    assert response.email == "gavin@overdue.test"
    assert response.amount_cents == 19955
    assert response.amount_currency == "EUR"
    assert response.payment_status == "pending"
    assert response.customer.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert len(response.invoices.__root__) == 2
    assert response.invoices.__root__[0].lago_id == "f8e194df-5d90-4382-b146-c881d2c67f28"
    assert response.invoices.__root__[1].lago_id == "a20b1805-d54c-4e57-873d-721cc153035e"


def test_invalid_create_payment_request_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/payment_requests",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.payment_requests.create(payment_request_object())
