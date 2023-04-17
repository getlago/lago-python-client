import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import AppliedCoupon


def create_applied_coupon():
    return AppliedCoupon(
        external_customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        coupon_code='Free-Lemon-Juice'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_coupon.json')

    with open(data_path, 'rb') as applied_coupon_response:
        return applied_coupon_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_coupon_index.json')

    with open(data_path, 'rb') as applied_coupon_response:
        return applied_coupon_response.read()


def test_valid_create_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/applied_coupons', content=mock_response())
    response = client.applied_coupons.create(create_applied_coupon())

    assert response.external_customer_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_invalid_create_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/applied_coupons', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.applied_coupons.create(create_applied_coupon())


def test_valid_find_all_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/applied_coupons', content=mock_collection_response())
    response = client.applied_coupons.find_all()

    assert response['applied_coupons'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_applied_coupon_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/applied_coupons?per_page=2&page=1', content=mock_collection_response())
    response = client.applied_coupons.find_all({'per_page': 2, 'page': 1})

    assert response['applied_coupons'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac2222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/applied_coupons', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.applied_coupons.find_all()


def test_valid_destroy_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    external_customer_id = 'external_customer_id'
    applied_coupon_id = '_ID_'

    httpx_mock.add_response(
        method='DELETE',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_coupons/' + applied_coupon_id,
        content=mock_response(),
    )
    response = client.applied_coupons.destroy(external_customer_id, applied_coupon_id)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_destroy_applied_coupon_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    external_customer_id = 'external_customer_id'
    applied_coupon_id = '_ID_'

    httpx_mock.add_response(
        method='DELETE',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_coupons/' + applied_coupon_id,
        status_code=404,
        content=b'',
    )
    with pytest.raises(LagoApiError):
        client.applied_coupons.destroy(external_customer_id, applied_coupon_id)
