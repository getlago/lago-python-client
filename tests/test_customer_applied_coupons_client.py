import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

from .utils.mixin import mock_response


def test_valid_find_all_customer_applied_coupons_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/applied_coupons",
        content=mock_response(mock="applied_coupon_index"),
    )
    response = client.customer_applied_coupons.find_all(resource_id="external_customer_id")

    assert response["applied_coupons"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_customer_applied_coupons_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/applied_coupons?per_page=2&page=1",
        content=mock_response(mock="applied_coupon_index"),
    )
    response = client.customer_applied_coupons.find_all(
        resource_id="external_customer_id", options={"per_page": 2, "page": 1}
    )

    assert response["applied_coupons"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/customers/external_customer_id/applied_coupons",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.customer_applied_coupons.find_all(resource_id="external_customer_id")
