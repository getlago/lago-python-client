import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.gross_revenue import GrossRevenueResponse


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/gross_revenue_index.json')

    with open(data_path, 'rb') as gross_revenues_response:
        return gross_revenues_response.read()


def test_valid_find_all_gross_revenues_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/analytics/gross_revenue', content=mock_collection_response())
    response = client.gross_revenues.find_all()

    assert response['gross_revenues'][0].currency == 'EUR'
    assert response['gross_revenues'][0].amount_cents == 100
    assert response['gross_revenues'][0].month == '2023-11-01T00:00:00.000Z'
