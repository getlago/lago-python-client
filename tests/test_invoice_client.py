import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import InvoiceStatusChange
from lago_python_client.clients.base_client import LagoApiError


def update_invoice_object():
    return InvoiceStatusChange(status='failed')


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/invoice.json')

    with open(my_data_path, 'r') as invoice_response:
        return invoice_response.read()


class TestInvoiceClient(unittest.TestCase):
    def test_valid_update_invoice_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
                           text=mock_response())
            response = client.invoices().update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

        self.assertEqual(response.lago_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response.status, 'failed')

    def test_invalid_update_invoice_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
                           status_code=401,
                           text='')

            with self.assertRaises(LagoApiError):
                client.invoices().update(update_invoice_object(), '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')


if __name__ == '__main__':
    unittest.main()
