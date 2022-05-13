import unittest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.models import Event
from lago_python_client.clients.base_client import LagoApiError


def create_event():
    return Event(customer_id='5eb02857-a71e-4ea2-bcf9-57d8885990ba', code='123', transaction_id='123')


class TestEventClient(unittest.TestCase):
    def test_valid_create_events_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/events', text='')
            response = client.events().create(create_event())

        self.assertEqual(response, True)

    def test_invalid_create_events_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/events', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.events().create(create_event())


if __name__ == '__main__':
    unittest.main()
