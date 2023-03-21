import os

import pytest
import requests_mock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/webhook.json')

    with open(data_path, 'r') as webhook_response:
        return webhook_response.read()


if True:
    def test_valid_public_key_request():
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/webhooks/json_public_key', text=mock_response())
            response = client.webhooks().public_key()

        assert response == b'key'


    def test_invalid_public_key_request():
        client = Client(api_key='invalid')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/webhooks/json_public_key', status_code=401, text='')

            with pytest.raises(LagoApiError):
                client.webhooks().public_key()
