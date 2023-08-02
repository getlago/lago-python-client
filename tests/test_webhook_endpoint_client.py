import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import WebhookEndpoint


def webhook_endpoint_object():
    return WebhookEndpoint(
        webhook_url='https://foo.bar',
        signature_algo='hmac'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/webhook_endpoint.json')

    with open(data_path, 'rb') as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/webhook_endpoint_index.json')

    with open(data_path, 'rb') as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def test_valid_create_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/webhook_endpoints', content=mock_response())
    response = client.webhook_endpoints.create(webhook_endpoint_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_create_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/webhook_endpoints', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.create(webhook_endpoint_object())


def test_valid_update_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, content=mock_response())
    response = client.webhook_endpoints.update(webhook_endpoint_object(), arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_update_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.update(webhook_endpoint_object(), arg)


def test_valid_find_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, content=mock_response())
    response = client.webhook_endpoints.find(arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_find_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.find(arg)


def test_valid_destroy_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, content=mock_response())
    response = client.webhook_endpoints.destroy(arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_destroy_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/webhook_endpoints/' + arg, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.destroy(arg)


def test_valid_find_all_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/webhook_endpoints', content=mock_collection_response())
    response = client.webhook_endpoints.find_all()

    assert response['webhook_endpoints'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response['meta']['current_page'] == 1

def test_invalid_find_all_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/webhook_endpoints', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.find_all()
