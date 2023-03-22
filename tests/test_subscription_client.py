import os

import pytest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Subscription


def create_subscription():
    return Subscription(external_customer_id='5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba', plan_code='eartha lynch',
                        external_id='code', billing_time='anniversary', subscription_date='2022-04-29')


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/subscription.json')

    with open(my_data_path, 'r') as subscription_response:
        return subscription_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/subscription_index.json')

    with open(data_path, 'r') as subscription_response:
        return subscription_response.read()


def test_valid_create_subscriptions_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/subscriptions', text=mock_response())
        response = client.subscriptions().create(create_subscription())

    assert response.external_customer_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.status == 'active'
    assert response.plan_code == 'eartha lynch'
    assert response.billing_time == 'anniversary'
    assert response.subscription_date == '2022-04-29'


def test_invalid_create_subscriptions_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('POST', 'https://api.getlago.com/api/v1/subscriptions', status_code=401, text='')

        with pytest.raises(LagoApiError):
            client.subscriptions().create(create_subscription())


def test_valid_update_subscription_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = 'sub_id'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/subscriptions/' + identifier,
                       text=mock_response())
        response = client.subscriptions().update(Subscription(name='name'), identifier)

    assert response.external_customer_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.status == 'active'
    assert response.plan_code == 'eartha lynch'
    assert response.billing_time == 'anniversary'
    assert response.subscription_date == '2022-04-29'


def test_invalid_update_subscription_request():
    client = Client(api_key='invalid')
    identifier = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('PUT',
                       'https://api.getlago.com/api/v1/subscriptions/' + identifier,
                       status_code=401,
                       text='')

        with pytest.raises(LagoApiError):
            client.subscriptions().update(Subscription(name='name'), identifier)


def test_valid_destroy_subscription_request():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = 'sub_id'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/subscriptions/' + identifier, text=mock_response())
        response = client.subscriptions().destroy(identifier)

    assert response.external_customer_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response.status == 'active'
    assert response.plan_code == 'eartha lynch'


def test_invalid_destroy_subscription_request():
    client = Client(api_key='invalid')
    identifier = 'invalid'

    with requests_mock.Mocker() as m:
        m.register_uri('DELETE', 'https://api.getlago.com/api/v1/subscriptions/' + identifier,
                       status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.subscriptions().destroy(identifier)


def test_valid_find_all_subscription_request_with_options():
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/subscriptions?external_customer_id=123',
                       text=mock_collection_response())
        response = client.subscriptions().find_all({'external_customer_id': '123'})

    assert response['subscriptions'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_subscription_request():
    client = Client(api_key='invalid')

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/subscriptions', status_code=404, text='')

        with pytest.raises(LagoApiError):
            client.subscriptions().find_all()
