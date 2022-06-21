import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Customer, BillingConfiguration
from lago_python_client.clients.base_client import LagoApiError


def create_customer():
    return Customer(
        customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        name='Gavin Belson',
        billing_configuration=BillingConfiguration(
            payment_provider='stripe',
            provider_customer_id='cus_12345'
        )
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/customer.json')

    with open(my_data_path, 'r') as customer_response:
        return customer_response.read()


class TestCustomerClient(unittest.TestCase):
    def test_valid_create_customers_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/customers', text=mock_response())
            response = client.customers().create(create_customer())

        self.assertEqual(response.customer_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response.name, 'Gavin Belson')
        self.assertEqual(response.email, 'dinesh@piedpiper.test')
        self.assertEqual(response.billing_configuration.payment_provider, 'stripe')
        self.assertEqual(response.billing_configuration.provider_customer_id, 'cus_12345')

    def test_invalid_create_customers_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/customers', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.customers().create(create_customer())


if __name__ == '__main__':
    unittest.main()
