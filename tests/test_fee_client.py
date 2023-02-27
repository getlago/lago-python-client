import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError

def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/fee.json')

    with open(my_data_path, 'r') as fee_response:
        return fee_response.read()

class TestFeeClient(unittest.TestCase):
  def test_valid_find_fee_request(self):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    with requests_mock.Mocker() as m:
        m.register_uri('GET', 'https://api.getlago.com/api/v1/fees/' + identifier, text=mock_response())
        response = client.fees().find(identifier)

    self.assertEqual(response.lago_id, identifier)
