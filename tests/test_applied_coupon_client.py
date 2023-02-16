import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import AppliedCoupon
from lago_python_client.clients.base_client import LagoApiError


def create_applied_coupon():
    return AppliedCoupon(
        external_customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba',
        coupon_code='Free-Lemon-Juice'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_coupon.json')

    with open(data_path, 'r') as applied_coupon_response:
        return applied_coupon_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/applied_coupon_index.json')

    with open(data_path, 'r') as applied_coupon_response:
        return applied_coupon_response.read()


class TestAppliedCouponClient(unittest.TestCase):
    def test_valid_create_applied_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/applied_coupons', text=mock_response())
            response = client.applied_coupons().create(create_applied_coupon())

        self.assertEqual(response.external_customer_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    def test_invalid_create_applied_coupon_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/applied_coupons', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.applied_coupons().create(create_applied_coupon())

    def test_valid_find_all_applied_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/applied_coupons', text=mock_collection_response())
            response = client.applied_coupons().find_all()

        self.assertEqual(response['applied_coupons'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_applied_coupon_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/applied_coupons?per_page=2&page=1', text=mock_collection_response())
            response = client.applied_coupons().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['applied_coupons'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac2222')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_applied_coupon_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/applied_coupons', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.applied_coupons().find_all()

    def test_valid_destroy_applied_coupon_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        external_customer_id = 'external_customer_id'
        applied_coupon_id = '_ID_'

        with requests_mock.Mocker() as m:
            m.register_uri(
                'DELETE',
                'https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_coupons/' + applied_coupon_id,
                text=mock_response()
            )
            response = client.applied_coupons().destroy(external_customer_id, applied_coupon_id)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')

    def test_invalid_destroy_applied_coupon_request(self):
        client = Client(api_key='invalid')
        external_customer_id = 'external_customer_id'
        applied_coupon_id = '_ID_'

        with requests_mock.Mocker() as m:
            m.register_uri(
                'DELETE',
                'https://api.getlago.com/api/v1/customers/' + external_customer_id + '/applied_coupons/' + applied_coupon_id,
                status_code=404,
                text=''
            )
            with self.assertRaises(LagoApiError):
                client.applied_coupons().destroy(external_customer_id, applied_coupon_id)

if __name__ == '__main__':
    unittest.main()
