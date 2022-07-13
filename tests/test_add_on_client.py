import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import AddOn
from lago_python_client.clients.base_client import LagoApiError


def add_on_object():
    return AddOn(
        name='name',
        code='add_on_first',
        amount_cents=1000,
        amount_currency='EUR',
        description='desc'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/add_on.json')

    with open(data_path, 'r') as add_on_response:
        return add_on_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/add_on_index.json')

    with open(data_path, 'r') as add_on_response:
        return add_on_response.read()


class TestAddOnClient(unittest.TestCase):
    def test_valid_create_add_on_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/add_ons', text=mock_response())
            response = client.add_ons().create(add_on_object())

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, 'add_on_code')

    def test_invalid_create_add_on_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/add_ons', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.add_ons().create(add_on_object())

    def test_valid_update_add_on_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'add_on_code'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/add_ons/' + code,
                           text=mock_response())
            response = client.add_ons().update(add_on_object(), code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_update_add_on_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/add_ons/' + code,
                           status_code=401,
                           text='')

            with self.assertRaises(LagoApiError):
                client.add_ons().update(add_on_object(), code)

    def test_valid_find_add_on_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'add_on_code'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/add_ons/' + code, text=mock_response())
            response = client.add_ons().find(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_find_add_on_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/add_ons/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.add_ons().find(code)

    def test_valid_destroy_add_on_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'add_on_code'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/add_ons/' + code, text=mock_response())
            response = client.add_ons().destroy(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_destroy_add_on_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/add_ons/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.add_ons().destroy(code)

    def test_valid_find_all_add_on_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/add_ons', text=mock_collection_response())
            response = client.add_ons().find_all()

        self.assertEqual(response['add_ons'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_add_on_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/add_ons?per_page=2&page=1', text=mock_collection_response())
            response = client.add_ons().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['add_ons'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1222')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_add_on_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/add_ons', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.add_ons().find_all()


if __name__ == '__main__':
    unittest.main()
