import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.applied_tax_rate import AppliedTaxRate


def applied_tax_rate_object():
    return AppliedTaxRate(
        tax_rate_code='tax_rate_code'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_tax_rate.json')

    with open(data_path, 'rb') as applied_tax_rate_response:
        return applied_tax_rate_response.read()


def test_valid_create_applied_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    external_customer_id = 'external_id'

    httpx_mock.add_response(
        method='POST',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_tax_rates',
        content=mock_response()
    )
    response = client.applied_tax_rates.create(external_customer_id, applied_tax_rate_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.tax_rate_code == 'tax_rate_code'


def test_invalid_create_applied_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    external_customer_id = 'external_customer_id'

    httpx_mock.add_response(
        method='POST',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_tax_rates',
        status_code=401,
        content=b''
    )

    with pytest.raises(LagoApiError):
        client.applied_tax_rates.create(external_customer_id, applied_tax_rate_object())


def test_valid_destroy_applied_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    external_customer_id = 'external_customer_id'
    tax_rate_code = 'tax_rate_code'

    httpx_mock.add_response(
        method='DELETE',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_tax_rates/' + tax_rate_code,
        content=mock_response()
    )
    response = client.applied_tax_rates.destroy(external_customer_id, tax_rate_code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.tax_rate_code == tax_rate_code


def test_invalid_destroy_applied_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    external_customer_id = 'external_customer_id'
    tax_rate_code = 'invalid'

    httpx_mock.add_response(
        method='DELETE',
        url='https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_tax_rates/' + tax_rate_code,
        status_code=404,
        content=b''
    )

    with pytest.raises(LagoApiError):
        client.applied_tax_rates.destroy(external_customer_id, tax_rate_code)
