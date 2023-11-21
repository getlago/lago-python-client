import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.invoiced_usage import InvoicedUsageResponse


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/invoiced_usage_index.json')

    with open(data_path, 'rb') as invoiced_usages_response:
        return invoiced_usages_response.read()


def test_valid_find_all_invoiced_usages_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/analytics/invoiced_usage', content=mock_collection_response())
    response = client.invoiced_usages.find_all()

    assert response['invoiced_usages'][0].currency == 'EUR'
    assert response['invoiced_usages'][0].amount_cents == 100
    assert response['invoiced_usages'][0].code == 'code'
    assert response['invoiced_usages'][0].month == '2023-11-01T00:00:00.000Z'
