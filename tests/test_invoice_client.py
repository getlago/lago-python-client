import os

import pytest
from pytest_httpx import HTTPXMock
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Invoice, InvoiceMetadata, InvoiceMetadataList


def update_invoice_object():
    metadata = InvoiceMetadata(key='key', value='value')
    metadata_list = InvoiceMetadataList(__root__=[metadata])

    return Invoice(payment_status='failed', metadata=metadata_list)


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/invoice.json')

    with open(my_data_path, 'rb') as invoice_response:
        return invoice_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/invoice_index.json')

    with open(data_path, 'rb') as invoice_response:
        return invoice_response.read()


def test_valid_update_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
                       text=mock_response())
        response = client.invoices().update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.status == 'finalized'
    assert response.payment_status == 'failed'
    assert response.metadata.__root__[0].key == 'key'
    assert response.metadata.__root__[0].value == 'value'


def test_invalid_update_invoice_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
                       status_code=401,
                       text='')

        with pytest.raises(LagoApiError):
            client.invoices().update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')


def test_valid_find_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices/' + identifier, text=mock_response())
        response = client.invoices().find(identifier)

    assert response.lago_id == identifier


def test_invalid_find_invoice_request():
    client = Client(api_key='invalid')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices/' + identifier, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.invoices().find(identifier)


def test_valid_find_all_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices', text=mock_collection_response())
        response = client.invoices().find_all()

    assert response['invoices'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_invoice_request_with_options():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices?per_page=2&page=1', text=mock_collection_response())
        response = client.invoices().find_all({'per_page': 2, 'page': 1})

    assert response['invoices'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_invoice_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices', status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.invoices().find_all()


def test_valid_download_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST',
                        'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/download',
                        text=mock_response())
        response = client.invoices().download('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_refresh_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                        'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/refresh',
                        text=mock_response())
        response = client.invoices().refresh('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_finalize_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                        'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/finalize',
                        text=mock_response())
        response = client.invoices().finalize('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_retry_payment_invoice_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri(
            'POST',
            'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/retry_payment',
            text=mock_response())
        response = client.invoices().retry_payment('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
