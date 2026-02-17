from pytest_httpx import HTTPXMock

from lago_python_client.client import Client


def mock_metadata_response():
    return b'{"metadata": {"foo": "bar", "baz": null}}'


def mock_null_metadata_response():
    return b'{"metadata": null}'


def test_valid_replace_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    customer_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    wallet_code = "wallet-code"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/customers/" + customer_id + "/wallets/" + wallet_code + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.customers.wallets.metadata.replace(customer_id, wallet_code, {"foo": "bar", "baz": None})

    assert response == {"foo": "bar", "baz": None}


def test_valid_merge_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    customer_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    wallet_code = "wallet-code"

    httpx_mock.add_response(
        method="PATCH",
        url="https://api.getlago.com/api/v1/customers/" + customer_id + "/wallets/" + wallet_code + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.customers.wallets.metadata.merge(customer_id, wallet_code, {"foo": "qux"})

    assert response == {"foo": "bar", "baz": None}


def test_valid_delete_all_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    customer_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    wallet_code = "wallet-code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/" + customer_id + "/wallets/" + wallet_code + "/metadata",
        content=mock_null_metadata_response(),
    )
    response = client.customers.wallets.metadata.delete_all(customer_id, wallet_code)

    assert response is None


def test_valid_delete_metadata_key_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    customer_id = "b7ab2926-1de8-4428-9bcd-779314ac129b"
    wallet_code = "wallet-code"
    key = "foo"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/customers/" + customer_id + "/wallets/" + wallet_code + "/metadata/" + key,
        content=b'{"metadata": {"baz": "qux"}}',
    )
    response = client.customers.wallets.metadata.delete_key(customer_id, wallet_code, key)

    assert response == {"baz": "qux"}
