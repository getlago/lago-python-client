import os

from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, 'fixtures/fee.json')

    with open(my_data_path, 'rb') as fee_response:
        return fee_response.read()


def test_valid_find_fee_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    fee_invoice_display_name = 'fee_invoice_display_name'
    charge_invoice_display_name = 'charge_invoice_display_name'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/fees/' + identifier, content=mock_response())
    response = client.fees.find(identifier)

    assert response.lago_id == identifier
    assert response.invoice_display_name == fee_invoice_display_name
    assert response.item.invoice_display_name == charge_invoice_display_name
