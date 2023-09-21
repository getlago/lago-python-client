import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Plan, Charge, Charges


def plan_object():
    charge = Charge(
        billable_metric_id='id',
        charge_model='standard',
        amount_currency='EUR',
        pay_in_advance=True,
        invoiceable=False,
        prorated=False,
        min_amount_cents=0,
        group_properties = [
            {
                'group_id': 'id',
                'values': {
                    'amount': '0.22'
                },
                'invoice_display_name': 'Europe'
            }
        ]
    )
    charges = Charges(__root__=[charge])

    return Plan(
        name='name',
        invoice_display_name='invoice_display_name',
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
        prorated=False,
        properties = {
            'graduated_ranges': [
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
        charges = charges,
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/plan.json')

    with open(data_path, 'rb') as plan_response:
        return plan_response.read()


def mock_graduated_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/graduated_plan.json')

    with open(data_path, 'rb') as plan_response:
        return plan_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/plan_index.json')

    with open(data_path, 'rb') as plan_response:
        return plan_response.read()


def test_valid_create_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/plans', content=mock_response())
    response = client.plans.create(plan_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'plan_code'
    assert response.invoice_display_name == 'test plan 1'
    assert response.charges.__root__[0].invoice_display_name == 'Setup'


def test_valid_create_graduated_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/plans', content=mock_graduated_response())
    response = client.plans.create(graduated_plan_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'plan_code'
    assert response.invoice_display_name == 'test plan 1'


def test_invalid_create_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/plans', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.plans.create(plan_object())


def test_valid_update_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/plans/' + code, content=mock_response())
    response = client.plans.update(plan_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code
    assert response.invoice_display_name == 'test plan 1'


def test_invalid_update_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/plans/' + code, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.plans.update(plan_object(), code)


def test_valid_find_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/plans/' + code, content=mock_response())
    response = client.plans.find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code
    assert response.invoice_display_name == 'test plan 1'
    assert response.charges.__root__[0].charge_model == 'standard'
    assert response.charges.__root__[0].min_amount_cents == 0


def test_invalid_find_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/plans/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.plans.find(code)


def test_valid_destroy_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/plans/' + code, content=mock_response())
    response = client.plans.destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    code = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/plans/' + code, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.plans.destroy(code)


def test_valid_find_all_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/plans', content=mock_collection_response())
    response = client.plans.find_all()

    assert response['plans'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['plans'][0].invoice_display_name == 'test plan 1'
    assert response['plans'][0].charges.__root__[0].lago_id == '51c1e851-5be6-4343-a0ee-39a81d8b4ee1'
    assert response['plans'][0].charges.__root__[0].group_properties.__root__[0].group_id == 'gfc1e851-5be6-4343-a0ee-39a81d8b4ee1'
    assert response['plans'][0].charges.__root__[0].group_properties.__root__[0].values['amount'] == '0.22'
    assert response['plans'][0].charges.__root__[0].group_properties.__root__[0].invoice_display_name == 'Europe'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_plan_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/plans?per_page=2&page=1', content=mock_collection_response())
    response = client.plans.find_all({'per_page': 2, 'page': 1})

    assert response['plans'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/plans', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.plans.find_all()
