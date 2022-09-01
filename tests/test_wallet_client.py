import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Wallet
from lago_python_client.clients.base_client import LagoApiError


def wallet_object():
    return Wallet(
        name='name',
        external_customer_id='12345',
        rate_amount='1',
        paid_credits='10',
        granted_credits='10'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet.json')

    with open(data_path, 'r') as wallet_response:
        return wallet_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet_index.json')

    with open(data_path, 'r') as wallet_response:
        return wallet_response.read()


class TestWalletClient(unittest.TestCase):
    def test_valid_create_wallet_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/wallets', text=mock_response())
            response = client.wallets().create(wallet_object())

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')

    def test_invalid_create_wallet_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/wallets', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.wallets().create(wallet_object())

    def test_valid_update_wallet_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/wallets/' + arg,
                           text=mock_response())
            response = client.wallets().update(wallet_object(), arg)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')

    def test_invalid_update_wallet_request(self):
        client = Client(api_key='invalid')
        arg = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/wallets/' + arg,
                           status_code=401,
                           text='')

            with self.assertRaises(LagoApiError):
                client.wallets().update(wallet_object(), arg)

    def test_valid_find_wallet_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/wallets/' + arg, text=mock_response())
            response = client.wallets().find(arg)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')

    def test_invalid_find_wallet_request(self):
        client = Client(api_key='invalid')
        arg = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/wallets/' + arg, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.wallets().find(arg)

    def test_valid_destroy_wallet_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/wallets/' + arg, text=mock_response())
            response = client.wallets().destroy(arg)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')

    def test_invalid_destroy_wallet_request(self):
        client = Client(api_key='invalid')
        arg = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/wallets/' + arg, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.wallets().destroy(arg)

    def test_valid_find_all_wallet_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/wallets', text=mock_collection_response())
            response = client.wallets().find_all()

        self.assertEqual(response['wallets'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_wallet_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/wallets?external_customer_id=123&per_page=2&page=1', text=mock_collection_response())
            response = client.wallets().find_all({'external_customer_id': 123, 'per_page': 2, 'page': 1})

        self.assertEqual(response['wallets'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_wallet_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/wallets', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.wallets().find_all()


if __name__ == '__main__':
    unittest.main()
