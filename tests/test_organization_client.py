import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Organization, OrganizationBillingConfiguration


def organization_object():
    return Organization(
        webhook_url="https://test-example.example",
        webhook_urls=["https://test-example.example", "https://test-example2.example"],
        tax_identification_number='EU123456789',
        net_payment_term=0,
        default_currency='EUR',
        document_number_prefix='ORG-1234',
        billing_configuration=OrganizationBillingConfiguration(
            invoice_footer='footer',
            invoice_grace_period=3,
            vat_rate=20,
            document_locale="fr"
        )
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/organization.json')

    with open(data_path, 'rb') as organization_response:
        return organization_response.read()


def test_valid_update_organization_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/organizations', content=mock_response())
    response = client.organizations.update(organization_object())

    assert response.name == 'Hooli'
    assert response.tax_identification_number == 'EU123456789'
    assert response.document_number_prefix == 'ORG-1234'
    assert response.net_payment_term == 0


def test_invalid_update_organization_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/organizations', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.organizations.update(organization_object())
