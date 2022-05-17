import unittest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.clients.base_client import LagoApiError


class TestWebhookClient(unittest.TestCase):
    def test_valid_public_key_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/webhooks/public_key', text='a2V5')
            response = client.webhooks().public_key()

        self.assertEqual(response, b'key')

    def test_invalid_public_key_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/webhooks/public_key', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.webhooks().public_key()


if __name__ == '__main__':
    unittest.main()
