import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Invoice, InvoiceMetadata, InvoiceMetadataList,\
    OneOffInvoice, InvoiceFeesList, InvoiceFee


def update_invoice_object():
    metadata = InvoiceMetadata(key='key', value='value')
    metadata_list = InvoiceMetadataList(__root__=[metadata])

    return Invoice(payment_status='failed', metadata=metadata_list)


def one_off_invoice_object():
    fee = InvoiceFee(add_on_code='123', description='desc')
    fees_list = InvoiceFeesList(__root__=[fee])

    return OneOffInvoice(customer_external_id='external', currency='EUR', fees=fees_list)


def mock_response(mock='invoice'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/' + mock + '.json')

    with open(my_data_path, 'rb') as invoice_response:
        return invoice_response.read()


def test_valid_update_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba', content=mock_response())
    response = client.invoices.update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.status == 'finalized'
    assert response.payment_status == 'failed'
    assert response.metadata.__root__[0].key == 'key'
    assert response.metadata.__root__[0].value == 'value'


def test_valid_create_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/invoices', content=mock_response(mock='one_off_invoice'))
    response = client.invoices.create(one_off_invoice_object())

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.invoice_type == 'one_off'
    assert response.fees.__root__[0].invoice_display_name == 'fee_invoice_display_name'
    assert response.fees.__root__[0].precise_unit_amount == '9.52'
    assert response.fees.__root__[0].item.invoice_display_name == 'one_off_invoice_display_name'
    assert response.fees.__root__[0].amount_details == {}


def test_invalid_create_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/invoices', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.invoices.create(one_off_invoice_object())


def test_invalid_update_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.invoices.update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')


def test_valid_find_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/invoices/' + identifier, content=mock_response())
    response = client.invoices.find(identifier)

    assert response.lago_id == identifier


def test_invalid_find_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/invoices/' + identifier, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.invoices.find(identifier)


def test_valid_find_all_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/invoices', content=mock_response(mock='invoice_index'))
    response = client.invoices.find_all()

    assert response['invoices'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_invoice_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/invoices?per_page=2&page=1', content=mock_response(mock='invoice_index'))
    response = client.invoices.find_all({'per_page': 2, 'page': 1})

    assert response['invoices'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/invoices', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.invoices.find_all()


def test_valid_download_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/download', content=mock_response())
    response = client.invoices.download('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_refresh_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/refresh', content=mock_response())
    response = client.invoices.refresh('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_finalize_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/finalize', content=mock_response())
    response = client.invoices.finalize('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_retry_payment_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='POST',
        url='https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/retry_payment',
        content=mock_response(),
    )
    response = client.invoices.retry_payment('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
