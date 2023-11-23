import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.invoice_collection import InvoiceCollectionResponse


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/invoice_collection_index.json')

    with open(data_path, 'rb') as invoice_collections_response:
        return invoice_collections_response.read()


def test_valid_find_all_invoice_collections_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/analytics/invoice_collection', content=mock_collection_response())
    response = client.invoice_collections.find_all()

    assert response['invoice_collections'][0].currency == 'EUR'
    assert response['invoice_collections'][0].amount_cents == 100
    assert response['invoice_collections'][0].month == '2023-11-01T00:00:00.000Z'
    assert response['invoice_collections'][0].invoices_count == 10
    assert response['invoice_collections'][0].payment_status == 'pending'
