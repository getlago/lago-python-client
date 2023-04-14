import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Customer, CustomerBillingConfiguration, Metadata, MetadataList


def create_customer():
    metadata = Metadata(
        display_in_invoice=True,
        key='key',
        value='value'
    )
    metadata_list = MetadataList(__root__=[metadata])

    return Customer(
        external_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        name='Gavin Belson',
        currency='EUR',
        billing_configuration=CustomerBillingConfiguration(
            invoice_grace_period=3,
            payment_provider='stripe',
            provider_customer_id='cus_12345',
            sync_with_provider=True,
            vat_rate=12.5,
            document_locale="fr"
        ),
        metadata=metadata_list
    )


def mock_response(mock='customer'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/' + mock + '.json')

    with open(my_data_path, 'rb') as customer_response:
        return customer_response.read()


def test_valid_create_customers_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/customers', content=mock_response())
    response = client.customers.create(create_customer())

    assert response.external_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.name == 'Gavin Belson'
    assert response.email == 'dinesh@piedpiper.test'
    assert response.currency == 'EUR'
    assert response.billing_configuration.invoice_grace_period == 3
    assert response.billing_configuration.payment_provider == 'stripe'
    assert response.billing_configuration.provider_customer_id == 'cus_12345'
    assert response.billing_configuration.sync_with_provider == True
    assert response.billing_configuration.vat_rate == 12.5
    assert response.billing_configuration.document_locale == "fr"
    assert response.metadata.__root__[0].key == 'key'
    assert response.metadata.__root__[0].value == 'value'


def test_invalid_create_customers_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/customers', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.customers.create(create_customer())


def test_valid_current_usage(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='GET',
        url='https://api.getlago.com/api/v1/customers/external_customer_id/current_usage?external_subscription_id=123',
        content=mock_response('customer_usage'),
    )
    response = client.customers.current_usage('external_customer_id', '123')

    assert response.from_datetime == '2022-07-01T00:00:00Z'
    assert len(response.charges_usage) == 1
    assert response.charges_usage[0].units == 1.0


def test_invalid_current_usage(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='GET',
        url='https://api.getlago.com/api/v1/customers/invalid_customer/current_usage?external_subscription_id=123',
        status_code=404,
        content=b'',
    )

    with pytest.raises(LagoApiError):
        client.customers.current_usage('invalid_customer', '123')


def test_valid_portal_url(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='GET',
        url='https://api.getlago.com/api/v1/customers/external_customer_id/portal_url',
        content=mock_response('customer_portal_url'),
    )
    response = client.customers.portal_url('external_customer_id')

    assert response == "https://app.lago.dev/customer-portal/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaWt3WkdGbE1qWmxZUzFqWlRnekxUUTJZell0T1dRNFl5MHdabVF4TURabFlqY3dNVElHT2daRlZBPT0iLCJleHAiOiIyMDIzLTAzLTIzVDIzOjAzOjAwLjM2NloiLCJwdXIiOm51bGx9fQ==--7128c6e541adc7b4c14249b1b18509f92e652d17"


def test_invalid_portal_url(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/customers/invalid_customer/portal_url', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.customers.portal_url('invalid_customer')


def test_valid_destroy_customer_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    external_id = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/customers/' + external_id, content=mock_response())
    response = client.customers.destroy(external_id)

    assert response.lago_id == '99a6094e-199b-4101-896a-54e927ce7bd7'
    assert response.external_id == external_id


def test_invalid_destroy_customer_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    external_id = 'external_id'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/customers/' + external_id, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.customers.destroy(external_id)
