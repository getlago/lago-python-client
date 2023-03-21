import os

import pytest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Coupon, LimitationConfiguration


def coupon_object():
    return Coupon(
        name='name',
        code='code_first',
        amount_cents=1000,
        amount_currency='EUR',
        expiration='no_expiration',
        expiration_at="2022-08-08T23:59:59Z",
        coupon_type="fixed_amount",
        reusable=False,
        frequency="once",
        applies_to=LimitationConfiguration(plan_codes=['plan1'])
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


def test_valid_create_coupon_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/coupons', text=mock_response())
        response = client.coupons().create(coupon_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'coupon_code'


def test_invalid_create_coupon_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/coupons', status_code=401, text='')

        with pytest.raises(LagoApiError):
            client.coupons().create(coupon_object())


def test_valid_update_coupon_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'coupon_code'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/coupons/' + code,
                       text=mock_response())
        response = client.coupons().update(coupon_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_update_coupon_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/coupons/' + code,
                       status_code=401,
                       text='')

        with pytest.raises(LagoApiError):
            client.coupons().update(coupon_object(), code)


def test_valid_find_coupon_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'coupon_code'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons/' + code, text=mock_response())
        response = client.coupons().find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_find_coupon_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.coupons().find(code)


def test_valid_destroy_coupon_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'coupon_code'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/coupons/' + code, text=mock_response())
        response = client.coupons().destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_coupon_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/coupons/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.coupons().destroy(code)


def test_valid_find_all_coupon_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons', text=mock_collection_response())
        response = client.coupons().find_all()

    assert response['coupons'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_coupon_request_with_options():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons?per_page=2&page=1', text=mock_collection_response())
        response = client.coupons().find_all({'per_page': 2, 'page': 1})

    assert response['coupons'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_coupon_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/coupons', status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.coupons().find_all()
