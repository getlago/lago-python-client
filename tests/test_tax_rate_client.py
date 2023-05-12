import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.tax_rate import TaxRate


def tax_rate_object():
    return TaxRate(
        name='name',
        code='tax_rate_first',
        value=15.0,
        description='desc',
        applied_by_default=False
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/tax_rate.json')

    with open(data_path, 'rb') as tax_rate_response:
        return tax_rate_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/tax_rate_index.json')

    with open(data_path, 'rb') as tax_rate_response:
        return tax_rate_response.read()


def test_valid_create_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/tax_rates', content=mock_response())
    response = client.tax_rates.create(tax_rate_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'tax_rate_code'


def test_invalid_create_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/tax_rates', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.tax_rates.create(tax_rate_object())


def test_valid_update_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_rate_code'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/tax_rates/' + code, content=mock_response())
    response = client.tax_rates.update(tax_rate_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_update_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/tax_rates/' + code, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.tax_rates.update(tax_rate_object(), code)


def test_valid_find_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_rate_code'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/tax_rates/' + code, content=mock_response())
    response = client.tax_rates.find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_find_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/tax_rates/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.tax_rates.find(code)


def test_valid_destroy_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_rate_code'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/tax_rates/' + code, content=mock_response())
    response = client.tax_rates.destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/tax_rates/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.tax_rates.destroy(code)


def test_valid_find_all_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/tax_rates', content=mock_collection_response())
    response = client.tax_rates.find_all()

    assert response['tax_rates'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_tax_rate_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/tax_rates?per_page=2&page=1', content=mock_collection_response())
    response = client.tax_rates.find_all({'per_page': 2, 'page': 1})

    assert response['tax_rates'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_tax_rate_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/tax_rates', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.tax_rates.find_all()
