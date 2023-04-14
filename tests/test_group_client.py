import os

from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/group_index.json')

    with open(data_path, 'rb') as groups_response:
        return groups_response.read()


def test_valid_find_all_groups_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='GET',
        url='https://api.getlago.com/api/v1/billable_metrics/bm_code/groups?per_page=2&page=1',
        content=mock_collection_response(),
    )
    response = client.groups.find_all('bm_code', {'per_page': 2, 'page': 1})

    assert response['groups'][0].lago_id == '12345678-1de8-4428-9bcd-779314ac1111'
    assert response['meta']['current_page'] == 1
