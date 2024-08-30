import os

from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "fixtures/overdue_balance_index.json")

    with open(data_path, "rb") as overdue_balances_response:
        return overdue_balances_response.read()


def test_valid_find_all_overdue_balances_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/analytics/overdue_balance",
        content=mock_collection_response(),
    )
    response = client.overdue_balances.find_all()

    assert response["overdue_balances"][0].currency == "EUR"
    assert response["overdue_balances"][0].amount_cents == 100
    assert response["overdue_balances"][0].month == "2023-11-01T00:00:00.000Z"
    assert response["overdue_balances"][0].lago_invoice_ids == ["1a901a90-1a90-1a90-1a90-1a901a901a90"]
