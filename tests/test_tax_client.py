import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.tax import Tax


def tax_object():
    return Tax(
        name='name',
        code='tax_first',
        rate=15.0,
        description='desc',
        applied_to_organization=False
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/tax.json')

    with open(data_path, 'rb') as tax_response:
        return tax_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/tax_index.json')

    with open(data_path, 'rb') as tax_response:
        return tax_response.read()


def test_valid_create_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/taxes', content=mock_response())
    response = client.taxes.create(tax_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'tax_code'


def test_invalid_create_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/taxes', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.taxes.create(tax_object())


def test_valid_update_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_code'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/taxes/' + code, content=mock_response())
    response = client.taxes.update(tax_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_update_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/taxes/' + code, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.taxes.update(tax_object(), code)


def test_valid_find_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_code'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/taxes/' + code, content=mock_response())
    response = client.taxes.find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_find_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/taxes/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.taxes.find(code)


def test_valid_destroy_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'tax_code'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/taxes/' + code, content=mock_response())
    response = client.taxes.destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_tax_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/taxes/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.taxes.destroy(code)


def test_valid_find_all_taxes_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/taxes', content=mock_collection_response())
    response = client.taxes.find_all()

    assert response['taxes'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_taxes_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/taxes?per_page=2&page=1', content=mock_collection_response())
    response = client.taxes.find_all({'per_page': 2, 'page': 1})

    assert response['taxes'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_taxes_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/taxes', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.taxes.find_all()
