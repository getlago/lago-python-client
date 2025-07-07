import os

from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "fixtures/usage_index.json")

    with open(data_path, "rb") as invoiced_usages_response:
        return invoiced_usages_response.read()


def test_valid_find_all_invoiced_usages_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/analytics/usage",
        content=mock_collection_response(),
    )
    response = client.usages.find_all()

    assert response["usages"][0].amount_currency == "USD"
    assert response["usages"][0].amount_cents == 110
