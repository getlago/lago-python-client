import unittest
import requests_mock
import os

from lago_python_client.client import Client

def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/group_index.json')

    with open(data_path, 'r') as groups_response:
        return groups_response.read()

class TestGroupClient(unittest.TestCase):
    def test_valid_find_all_groups_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/billable_metrics/bm_code/groups', text=mock_collection_response())
            response = client.groups().find_all('bm_code', {'per_page': 2, 'page': 1})

        self.assertEqual(response['groups'][0].lago_id, '12345678-1de8-4428-9bcd-779314ac1111')
        self.assertEqual(response['meta']['current_page'], 1)


if __name__ == '__main__':
    unittest.main()
