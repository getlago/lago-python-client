import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Subscription
from lago_python_client.clients.base_client import LagoApiError


def create_subscription():
    return Subscription(customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba', plan_code='eartha lynch')


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/subscription.json')

    with open(my_data_path, 'r') as subscription_response:
        return subscription_response.read()


class TestSubscriptionClient(unittest.TestCase):
    def test_valid_create_subscriptions_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', '/api/v1/subscriptions', text=mock_response())
            response = client.subscriptions().create(create_subscription())

        self.assertEqual(response.customer_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response.status, 'active')
        self.assertEqual(response.plan_code, 'eartha lynch')

    def test_invalid_create_subscriptions_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', '/api/v1/subscriptions', status_code=401, text='')

        with self.assertRaises(LagoApiError):
            client.subscriptions().create(create_subscription())

    def test_valid_delete_subscriptions_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        params = {
            'customer_id': '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
        }

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', '/api/v1/subscriptions', text=mock_response())
            response = client.subscriptions().delete(params)

        self.assertEqual(response.customer_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response.status, 'active')
        self.assertEqual(response.plan_code, 'eartha lynch')

    def test_invalid_delete_subscriptions_request(self):
        client = Client(api_key='invalid')
        params = {
            'customer_id': 'invalid'
        }

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', '/api/v1/subscriptions', status_code=422, text='')

        with self.assertRaises(LagoApiError):
            client.subscriptions().delete(params)


if __name__ == '__main__':
    unittest.main()
