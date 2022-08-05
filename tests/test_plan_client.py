import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models import Plan, Charge, Charges
from lago_python_client.clients.base_client import LagoApiError


def plan_object():
    charge = Charge(
        billable_metric_id='id',
        charge_model='standard',
        amount_currency='EUR',
        properties={
            'amount': '0.22'
        }
    )
    charges = Charges(__root__=[charge])

    return Plan(
        name='name',
        code='code_first',
        amount_cents=1000,
        amount_currency='EUR',
        description='desc',
        interval='weekly',
        pay_in_advance=True,
        charges=charges
    )

def graduated_plan_object():
    charge = Charge(
        billable_metric_id='id',
        charge_model='graduated',
        amount_currency='EUR',
        properties = [
            {
                'to_value': 1,
                'from_value': 0,
                'flat_amount': "0",
                'per_unit_amount': "0"
            },
            {
                'to_value': None,
                'from_value': 2,
                'flat_amount': "0",
                'per_unit_amount': "3200"
            }
        ]
    )
    charges = Charges(__root__=[charge])

    return Plan(
        name='name',
        code='code_first',
        amount_cents=1000,
        amount_currency='EUR',
        description='desc',
        interval='weekly',
        pay_in_advance=True,
        charges = charges,
    )

def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/plan.json')

    with open(data_path, 'r') as plan_response:
        return plan_response.read()

def mock_graduated_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/graduated_plan.json')

    with open(data_path, 'r') as plan_response:
        return plan_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/plan_index.json')

    with open(data_path, 'r') as plan_response:
        return plan_response.read()


class TestPlanClient(unittest.TestCase):
    def test_valid_create_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', text=mock_response())
            response = client.plans().create(plan_object())

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, 'plan_code')

    def test_valid_create_graduated_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', text=mock_graduated_response())
            response = client.plans().create(graduated_plan_object())
        
        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, 'plan_code')

    def test_invalid_create_plan_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', status_code=401, text='')

            with self.assertRaises(LagoApiError):
                client.plans().create(plan_object())

    def test_valid_update_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'plan_code'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/plans/' + code,
                           text=mock_response())
            response = client.plans().update(plan_object(), code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_update_plan_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/plans/' + code,
                           status_code=401,
                           text='')

            with self.assertRaises(LagoApiError):
                client.plans().update(plan_object(), code)

    def test_valid_find_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'plan_code'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/plans/' + code, text=mock_response())
            response = client.plans().find(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)
        self.assertEqual(response.charges.__root__[0].charge_model, 'standard')

    def test_invalid_find_plan_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/plans/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.plans().find(code)

    def test_valid_destroy_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        code = 'plan_code'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/plans/' + code, text=mock_response())
            response = client.plans().destroy(code)

        self.assertEqual(response.lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac129b')
        self.assertEqual(response.code, code)

    def test_invalid_destroy_plan_request(self):
        client = Client(api_key='invalid')
        code = 'invalid'

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', 'https://api.getlago.com/api/v1/plans/' + code, status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.plans().destroy(code)

    def test_valid_find_all_plan_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/plans', text=mock_collection_response())
            response = client.plans().find_all()

        self.assertEqual(response['plans'][0].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_find_all_plan_request_with_options(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/plans?per_page=2&page=1', text=mock_collection_response())
            response = client.plans().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['plans'][1].lago_id, 'b7ab2926-1de8-4428-9bcd-779314ac1222')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_invalid_find_all_plan_request(self):
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/plans', status_code=404, text='')

            with self.assertRaises(LagoApiError):
                client.plans().find_all()


if __name__ == '__main__':
    unittest.main()
