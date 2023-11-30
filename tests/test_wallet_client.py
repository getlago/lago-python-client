import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Wallet, RecurringTransactionRule, RecurringTransactionRuleList


def wallet_object():
    rule = RecurringTransactionRule(
        rule_type='interval',
        interval='monthly',
        paid_credits='105.0',
        granted_credits='105.0',
    )
    rules_list = RecurringTransactionRuleList(__root__=[rule])
    return Wallet(
        name='name',
        external_customer_id='12345',
        rate_amount='1',
        paid_credits='10',
        granted_credits='10',
        recurring_transaction_rules=rules_list
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet.json')

    with open(data_path, 'rb') as wallet_response:
        return wallet_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet_index.json')

    with open(data_path, 'rb') as wallet_response:
        return wallet_response.read()


def test_valid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/wallets', content=mock_response())
    response = client.wallets.create(wallet_object())

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response.recurring_transaction_rules.__root__[0].lago_id == '12345'
    assert response.recurring_transaction_rules.__root__[0].rule_type == 'interval'
    assert response.recurring_transaction_rules.__root__[0].interval == 'monthly'


def test_invalid_create_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/wallets', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.wallets.create(wallet_object())


def test_valid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/wallets/' + arg, content=mock_response())
    response = client.wallets.update(wallet_object(), arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_update_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/wallets/' + arg, status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.wallets.update(wallet_object(), arg)


def test_valid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/wallets/' + arg, content=mock_response())
    response = client.wallets.find(arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_find_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/wallets/' + arg, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.wallets.find(arg)


def test_valid_destroy_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    arg = 'b7ab2926-1de8-4428-9bcd-779314ac129b'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/wallets/' + arg, content=mock_response())
    response = client.wallets.destroy(arg)

    assert response.lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'


def test_invalid_destroy_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    arg = 'invalid'

    httpx_mock.add_response(method='DELETE', url='https://api.getlago.com/api/v1/wallets/' + arg, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.wallets.destroy(arg)


def test_valid_find_all_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/wallets', content=mock_collection_response())
    response = client.wallets.find_all()

    assert response['wallets'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac129b'
    assert response['meta']['current_page'] == 1


def test_valid_find_all_wallet_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='GET',
        url='https://api.getlago.com/api/v1/wallets?external_customer_id=123&per_page=2&page=1',
        content=mock_collection_response(),
    )
    response = client.wallets.find_all({'external_customer_id': 123, 'per_page': 2, 'page': 1})

    assert response['wallets'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1


def test_invalid_find_all_wallet_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/wallets', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.wallets.find_all()
