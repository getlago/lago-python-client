from copy import deepcopy
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.models import PaymentFilters

from .utils.mixin import mock_response


@pytest.mark.parametrize("customer_scoped", [False, True])
def test_payment_filters_serialize_exactly(httpx_mock: HTTPXMock, customer_scoped):
    options: PaymentFilters = {
        "page": 2,
        "per_page": 5,
        "invoice_id": "1a901a90-1a90-1a90-1a90-1a901a901a90",
        "payment_status": ["succeeded", "failed"],
        "payment_statuses": ["pending"],
        "amount_from": 0,
        "amount_to": 9223372036854775807,
        "receipt_number": "Rcpt & +/#1",
        "created_at_from": "2026-09-01",
        "created_at_to": "2026-09-07",
        "payment_provider_type": ["stripe", "gocardless"],
        "currency": "EUR",
        "invoice_number": "LAG & +/#2",
        "payment_type": ["manual", "provider"],
        "payable_type": ["Invoice", "PaymentRequest"],
        "search_term": "pi_3 & +/#",
    }
    if not customer_scoped:
        options["external_customer_id"] = "cust_1"
    original = deepcopy(options)
    client = Client(api_key="test_key")
    httpx_mock.add_response(content=mock_response(mock="payment_index"))
    timeout = httpx.Timeout(17)
    if customer_scoped:
        result = client.customer_payments.find_all("cust_1", options, timeout)
    else:
        result = client.payments.find_all(options, timeout)
    request = httpx_mock.get_request()
    query = parse_qs(urlparse(str(request.url)).query)
    expected = {
        "page": ["2"],
        "per_page": ["5"],
        "invoice_id": ["1a901a90-1a90-1a90-1a90-1a901a901a90"],
        "payment_status[]": ["succeeded", "failed"],
        "payment_statuses[]": ["pending"],
        "amount_from": ["0"],
        "amount_to": ["9223372036854775807"],
        "receipt_number": ["Rcpt & +/#1"],
        "created_at_from": ["2026-09-01"],
        "created_at_to": ["2026-09-07"],
        "payment_provider_type[]": ["stripe", "gocardless"],
        "currency": ["EUR"],
        "invoice_number": ["LAG & +/#2"],
        "payment_type[]": ["manual", "provider"],
        "payable_type[]": ["Invoice", "PaymentRequest"],
        "search_term": ["pi_3 & +/#"],
    }
    if not customer_scoped:
        expected["external_customer_id"] = ["cust_1"]
    assert query == expected
    assert request.url.path == ("/api/v1/customers/cust_1/payments" if customer_scoped else "/api/v1/payments")
    assert request.headers["Authorization"] == "Bearer test_key"
    assert request.extensions["timeout"]["read"] == 17
    assert options == original
    assert result["meta"]["current_page"] == 1


@pytest.mark.parametrize(
    "options, expected",
    [
        ({"payment_status": "processing"}, {"payment_status": ["processing"]}),
        ({"payment_status[]": ["succeeded", "failed"]}, {"payment_status[]": ["succeeded", "failed"]}),
        (
            [("payment_status[]", "succeeded"), ("payment_status[]", "failed")],
            {"payment_status[]": ["succeeded", "failed"]},
        ),
        ({"payment_type": []}, {}),
    ],
)
def test_payment_filter_options_remain_compatible(httpx_mock: HTTPXMock, options, expected):
    httpx_mock.add_response(content=mock_response(mock="payment_index"))
    Client(api_key="test_key").payments.find_all(options)
    assert parse_qs(urlparse(str(httpx_mock.get_request().url)).query) == expected


def test_provider_payment_without_reference(httpx_mock: HTTPXMock):
    import json

    data = json.loads(mock_response(mock="payment_index"))
    data["payments"][0]["reference"] = None
    data["payments"][0]["type"] = "provider"
    httpx_mock.add_response(json=data)
    result = Client(api_key="test_key").payments.find_all({"payment_type": ["provider"]})
    assert result["payments"][0].reference is None
