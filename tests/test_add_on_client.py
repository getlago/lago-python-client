import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.add_on import AddOn


def add_on_object():
    return AddOn(
        name='name',
        invoice_display_name='add_on_invoice_display_name',
        code='add_on_first',
        amount_cents=1000,
        amount_currency='EUR',
        description='desc'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/add_on.json')

    with open(data_path, 'rb') as add_on_response:
        return add_on_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/add_on_index.json')

    with open(data_path, 'rb') as add_on_response:
        return add_on_response.read()


def test_valid_create_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/add_ons', content=mock_response())
    response = client.add_ons.create(add_on_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'add_on_code'
    assert response.invoice_display_name == 'add_on_invoice_display_name'


def test_invalid_create_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/add_ons', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.add_ons.create(add_on_object())


def test_valid_update_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'add_on_code'
    invoice_display_name = 'add_on_invoice_display_name'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/add_ons/' + code, content=mock_response())
    response = client.add_ons.update(add_on_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code
    assert response.invoice_display_name == invoice_display_name


def test_invalid_update_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/add_ons/' + code, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.add_ons.update(add_on_object(), code)


def test_valid_find_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'add_on_code'
    invoice_display_name = 'add_on_invoice_display_name'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/add_ons/' + code, content=mock_response())
    response = client.add_ons.find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code
    assert response.invoice_display_name == invoice_display_name



def test_invalid_find_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/add_ons/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.add_ons.find(code)


def test_valid_destroy_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'add_on_code'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/add_ons/' + code, content=mock_response())
    response = client.add_ons.destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/add_ons/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.add_ons.destroy(code)


def test_valid_find_all_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/add_ons', content=mock_collection_response())
    response = client.add_ons.find_all()

    assert response['add_ons'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_add_on_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/add_ons?per_page=2&page=1', content=mock_collection_response())
    response = client.add_ons.find_all({'per_page': 2, 'page': 1})

    assert response['add_ons'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/add_ons', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.add_ons.find_all()
