import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import WalletTransaction


def wallet_transaction_object():
    return WalletTransaction(
        wallet_id='123',
        paid_credits='10',
        granted_credits='10'
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/wallet_transaction.json')

    with open(data_path, 'rb') as wallet_transaction_response:
        return wallet_transaction_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/wallet_transaction_index.json')

    with open(data_path, 'rb') as wallet_transaction_index_response:
        return wallet_transaction_index_response.read()


def test_valid_create_wallet_transaction_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/wallet_transactions', content=mock_response())
    response = client.wallet_transactions.create(wallet_transaction_object())

    assert response['wallet_transactions'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['wallet_transactions'][1].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1222'


def test_invalid_create_wallet_transaction_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/wallet_transactions', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.wallet_transactions.create(wallet_transaction_object())


def test_valid_find_all_groups_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/wallets/555/wallet_transactions', content=mock_collection_response())
    response = client.wallet_transactions.find_all('555')

    assert response['wallet_transactions'][0].lago_id == 'b7ab2926-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1
