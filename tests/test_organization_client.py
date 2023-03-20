import os
import unittest

import pytest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Organization, OrganizationBillingConfiguration


def organization_object():
    return Organization(
        webhook_url="https://test-example.example",
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

    with open(data_path, 'r') as organization_response:
        return organization_response.read()


class TestOrganizationClient(unittest.TestCase):
    def test_valid_update_organization_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/organizations',
                           text=mock_response())
            response = client.organizations().update(organization_object())

        self.assertEqual(response.name, 'Hooli')

    def test_invalid_update_organization_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/organizations',
                           status_code=401,
                           text='')

            with pytest.raises(LagoApiError):
                client.organizations().update(organization_object())
