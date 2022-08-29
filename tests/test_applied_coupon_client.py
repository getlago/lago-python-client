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


if __name__ == '__main__':
    unittest.main()
