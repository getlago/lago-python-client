import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Customer, CustomerBillingConfiguration
from lago_python_client.clients.base_client import LagoApiError


def create_customer():
    return Customer(
        external_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        name='Gavin Belson',
        currency='EUR',
        billing_configuration=CustomerBillingConfiguration(
            payment_provider='stripe',
            provider_customer_id='cus_12345',
            vat_rate=12.5
        )
    )

def mock_response(mock='customer'):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/' + mock + '.json')

    with open(my_data_path, 'r') as customer_response:
        return customer_response.read()

class TestCustomerClient(unittest.TestCase):
    def test_valid_create_customers_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/customers', text=mock_response())
            response = client.customers().create(create_customer())

        self.assertEqual(response.external_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response.name, 'Gavin Belson')
        self.assertEqual(response.email, 'dinesh@piedpiper.test')
        self.assertEqual(response.currency, 'EUR')
        self.assertEqual(response.billing_configuration.payment_provider, 'stripe')
        self.assertEqual(response.billing_configuration.provider_customer_id, 'cus_12345')
        self.assertEqual(response.billing_configuration.vat_rate, 12.5)

    def test_invalid_create_customers_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/customers', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.customers().create(create_customer())


    def test_valid_current_usage(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET',
                           'https://api.getlago.com/api/v1/customers/external_customer_id/current_usage?external_subscription_id=123',
                           text=mock_response('customer_usage'))
            response = client.customers().current_usage('external_customer_id', '123')

        self.assertEqual(response.from_date, '2022-07-01')
        self.assertEqual(len(response.charges_usage), 1)
        self.assertEqual(response.charges_usage[0].units, 1.0)

    def test_invalid_current_usage(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET',
                           'https://api.getlago.com/api/v1/customers/invalid_customer/current_usage?external_subscription_id=123',
                           status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.customers().current_usage('invalid_customer', '123')


if __name__ == '__main__':
    unittest.main()
