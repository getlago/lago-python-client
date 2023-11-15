import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.outstanding_invoice import OutstandingInvoiceResponse


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/outstanding_invoice_index.json')

    with open(data_path, 'rb') as outstanding_invoices_response:
        return outstanding_invoices_response.read()


def test_valid_find_all_outstanding_invoices_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/analytics/outstanding_invoices', content=mock_collection_response())
    response = client.outstanding_invoices.find_all()

    assert response['outstanding_invoices'][0].currency == 'EUR'
    assert response['outstanding_invoices'][0].amount_cents == 100
    assert response['outstanding_invoices'][0].month == '2023-11-01T00:00:00.000Z'
    assert response['outstanding_invoices'][0].invoices_count == 10
    assert response['outstanding_invoices'][0].payment_status == 'pending'
