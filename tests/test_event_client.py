import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Event
from lago_python_client.models import BatchEvent
from lago_python_client.clients.base_client import LagoApiError


def create_event():
    return Event(customer_id='5eb02857-a71e-4ea2-bcf9-57d8885990ba', code='123', transaction_id='123')

def create_batch_event():
    return BatchEvent(subscription_ids=['88u02857-a71e-4ea2-bcf9-57d8885990ba'], code='123', transaction_id='123')

def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/event.json')

    with open(data_path, 'r') as event_response:
        return event_response.read()

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

    def test_valid_create_batch_events_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/events/batch', text='')
            response = client.events().batch_create(create_batch_event())

        self.assertEqual(response, True)

    def test_invalid_create_batch_events_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/events/batch', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.events().batch_create(create_batch_event())

    def test_valid_find_event_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        event_id = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/events/' + event_id, text=mock_response())
            response = client.events().find(event_id)

        self.assertEqual(response.lago_id, event_id)

    def test_invalid_find_events_request(self):
        client = Client(api_key='invalid')
        event_id = 'INVALID_EVENT'

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/events', status_code=401, text='')
            m.register_uri('GET', 'https://api.getlago.com/api/v1/events/' + event_id, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.events().find(event_id)

if __name__ == '__main__':
    unittest.main()
