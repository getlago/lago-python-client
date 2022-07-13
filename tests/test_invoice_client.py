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


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/invoice_index.json')

    with open(data_path, 'r') as invoice_response:
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

    def test_valid_find_invoice_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices/' + identifier, text=mock_response())
            response = client.invoices().find(identifier)

        self.assertEqual(response.lago_id, identifier)

    def test_invalid_find_invoice_request(self):
        client = Client(api_key='invalid')
        identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices/' + identifier, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.invoices().find(identifier)

    def test_valid_find_all_invoice_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices', text=mock_collection_response())
            response = client.invoices().find_all()

        self.assertEqual(response['invoices'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_invoice_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices?per_page=2&page=1', text=mock_collection_response())
            response = client.invoices().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['invoices'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1222')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_invoice_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/invoices', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.invoices().find_all()

    def test_valid_download_invoice_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST',
                            'https://api.getlago.com/api/v1/invoices/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/download',
                            text=mock_response())
            response = client.invoices().download('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

        self.assertEqual(response.lago_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')


if __name__ == '__main__':
    unittest.main()
