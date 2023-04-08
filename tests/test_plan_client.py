import os

import pytest
from pytest_httpx import HTTPXMock
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Plan, Charge, Charges


def plan_object():
    charge = Charge(
        billable_metric_id='id',
        charge_model='standard',
        amount_currency='EUR',
        instant=True,
        group_properties = [
            {
                'group_id': 'id',
                'values': {
                    'amount': '0.22'
                }
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
        charges=charges
    )


def graduated_plan_object():
    charge = Charge(
        billable_metric_id='id',
        charge_model='graduated',
        amount_currency='EUR',
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


def test_valid_create_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', text=mock_response())
        response = client.plans().create(plan_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'plan_code'


def test_valid_create_graduated_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', text=mock_graduated_response())
        response = client.plans().create(graduated_plan_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'plan_code'


def test_invalid_create_plan_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/plans', status_code=401, text='')

        with pytest.raises(LagoApiError):
            client.plans().create(plan_object())


def test_valid_update_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/plans/' + code,
                       text=mock_response())
        response = client.plans().update(plan_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_update_plan_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/plans/' + code,
                       status_code=401,
                       text='')

        with pytest.raises(LagoApiError):
            client.plans().update(plan_object(), code)


def test_valid_find_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/plans/' + code, text=mock_response())
        response = client.plans().find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code
    assert response.charges.__root__[0].charge_model == 'standard'


def test_invalid_find_plan_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/plans/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.plans().find(code)


def test_valid_destroy_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'plan_code'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/plans/' + code, text=mock_response())
        response = client.plans().destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_plan_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/plans/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.plans().destroy(code)


def test_valid_find_all_plan_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/plans', text=mock_collection_response())
        response = client.plans().find_all()

    assert response['plans'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_plan_request_with_options():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/plans?per_page=2&page=1', text=mock_collection_response())
        response = client.plans().find_all({'per_page': 2, 'page': 1})

    assert response['plans'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_plan_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/plans', status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.plans().find_all()
