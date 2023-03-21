import os

import pytest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import BillableMetric, BillableMetricGroup


def billable_metric_object():
    return BillableMetric(
        name='name',
        code='code_first',
        description='desc',
        aggregation_type='sum_agg',
        field_name='amount_sum',
        group=group()
    )


def group():
    return BillableMetricGroup(key='country', values=['france', 'italy', 'spain'])


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/billable_metric.json')

    with open(data_path, 'r') as billable_metric_response:
        return billable_metric_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/billable_metric_index.json')

    with open(data_path, 'r') as billable_metric_response:
        return billable_metric_response.read()


def test_valid_create_billable_metric_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/billable_metrics', text=mock_response())
        response = client.billable_metrics().create(billable_metric_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == 'bm_code'
    assert response.group == group()


def test_invalid_create_billable_metric_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/billable_metrics', status_code=401, text='')

        with pytest.raises(LagoApiError):
            client.billable_metrics().create(billable_metric_object())


def test_valid_update_billable_metric_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'bm_code'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/billable_metrics/' + code,
                       text=mock_response())
        response = client.billable_metrics().update(billable_metric_object(), code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_update_billable_metric_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/billable_metrics/' + code,
                       status_code=401,
                       text='')

        with pytest.raises(LagoApiError):
            client.billable_metrics().update(billable_metric_object(), code)


def test_valid_find_billable_metric_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'bm_code'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics/' + code, text=mock_response())
        response = client.billable_metrics().find(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_find_billable_metric_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.billable_metrics().find(code)


def test_valid_destroy_billable_metric_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    code = 'bm_code'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/billable_metrics/' + code, text=mock_response())
        response = client.billable_metrics().destroy(code)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.code == code


def test_invalid_destroy_billable_metric_request():
    client = Client(api_key='invalid')
    code = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/billable_metrics/' + code, status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.billable_metrics().destroy(code)


def test_valid_find_all_billable_metric_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics', text=mock_collection_response())
        response = client.billable_metrics().find_all()

    assert response['billable_metrics'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1000'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_billable_metric_request_with_options():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics?per_page=2&page=1', text=mock_collection_response())
        response = client.billable_metrics().find_all({'per_page': 2, 'page': 1})

    assert response['billable_metrics'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314a11111'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_billable_metric_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics', status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.billable_metrics().find_all()
