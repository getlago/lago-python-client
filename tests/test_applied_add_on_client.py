import os

import pytest
from pytest_httpx import HTTPXMock
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import AppliedAddOn


def create_applied_add_on():
    return AppliedAddOn(
        external_customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        add_on_code='Free-Lemon-Juice'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_add_on.json')

    with open(data_path, 'rb') as applied_add_on_response:
        return applied_add_on_response.read()


def test_valid_create_applied_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/applied_add_ons', content=mock_response())
    response = client.applied_add_ons().create(create_applied_add_on())

    assert response.external_customer_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_invalid_create_applied_add_on_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/applied_add_ons', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.applied_add_ons().create(create_applied_add_on())
