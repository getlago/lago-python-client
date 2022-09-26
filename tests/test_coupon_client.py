import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Coupon
from lago_python_client.clients.base_client import LagoApiError


def coupon_object():
    return Coupon(
        name='name',
        code='code_first',
        amount_cents=1000,
        amount_currency='EUR',
        expiration='no_expiration',
        expiration_date="2022-08-08",
        coupon_type="fixed_amount",
        frequency="once"
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/coupon.json')

    with open(data_path, 'r') as coupon_response:
        return coupon_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/coupon_index.json')

    with open(data_path, 'r') as coupon_response:
        return coupon_response.read()


class TestCouponClient(unittest.TestCase):
    def test_valid_create_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/coupons', text=mock_response())
            response = client.coupons().create(coupon_object())

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, 'coupon_code')

    def test_invalid_create_coupon_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/coupons', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.coupons().create(coupon_object())

    def test_valid_update_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'coupon_code'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/coupons/' + code,
                           text=mock_response())
            response = client.coupons().update(coupon_object(), code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_update_coupon_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/coupons/' + code,
                           status_code=401,
                           text='')

            with self.assertRaises(LagoApiError):
                client.coupons().update(coupon_object(), code)

    def test_valid_find_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'coupon_code'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons/' + code, text=mock_response())
            response = client.coupons().find(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_find_coupon_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.coupons().find(code)

    def test_valid_destroy_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'coupon_code'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/coupons/' + code, text=mock_response())
            response = client.coupons().destroy(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_destroy_coupon_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/coupons/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.coupons().destroy(code)

    def test_valid_find_all_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons', text=mock_collection_response())
            response = client.coupons().find_all()

        self.assertEqual(response['coupons'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_coupon_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons?per_page=2&page=1', text=mock_collection_response())
            response = client.coupons().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['coupons'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1222')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_coupon_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.coupons().find_all()


if __name__ == '__main__':
    unittest.main()
