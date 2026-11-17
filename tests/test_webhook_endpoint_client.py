import json
import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import WebhookEndpoint, WebhookEndpointSigningKeyResponse


def webhook_endpoint_object():
    return WebhookEndpoint(
        webhook_url="https://foo.bar",
        signature_algo="hmac",
        name="My Webhook Endpoint",
        event_types=["customer.created"],
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/webhook_endpoint.json")

    with open(data_path, "rb") as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def mock_standard_webhooks_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/webhook_endpoint_standard_webhooks.json")

    with open(data_path, "rb") as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def mock_empty_signing_keys_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/webhook_endpoint_empty_signing_keys.json")

    with open(data_path, "rb") as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def assert_standard_webhooks_signing_keys(signing_keys):
    assert len(signing_keys) == 2
    assert all(isinstance(key, WebhookEndpointSigningKeyResponse) for key in signing_keys)
    assert signing_keys[0].lago_id == "5f0b0a8e-3c39-4a2f-9a8d-1d0c6b1e2a01"
    assert signing_keys[0].secret_key == "whsec_fake_test_secret_1"
    assert signing_keys[0].created_at == "2022-04-29T08:59:51Z"
    assert signing_keys[1].lago_id == "9c4e7d21-6b8f-4e0a-b5d3-2f1a7c9e3b02"
    assert signing_keys[1].secret_key == "whsec_fake_test_secret_2"
    assert signing_keys[1].created_at == "2022-05-03T10:15:00Z"


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/webhook_endpoint_index.json")

    with open(data_path, "rb") as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def mock_collection_standard_webhooks_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/webhook_endpoint_index_standard_webhooks.json")

    with open(data_path, "rb") as webhook_endpoint_response:
        return webhook_endpoint_response.read()


def test_valid_create_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        content=mock_response(),
    )
    response = client.webhook_endpoints.create(webhook_endpoint_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_create_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.create(webhook_endpoint_object())


def test_valid_update_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_response(),
    )
    response = client.webhook_endpoints.update(webhook_endpoint_object(), arg)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_update_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.update(webhook_endpoint_object(), arg)


def test_valid_find_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_response(),
    )
    response = client.webhook_endpoints.find(arg)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_find_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.find(arg)


def test_valid_destroy_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_response(),
    )
    response = client.webhook_endpoints.destroy(arg)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"


def test_invalid_destroy_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    arg = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.destroy(arg)


def test_valid_find_all_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        content=mock_collection_response(),
    )
    response = client.webhook_endpoints.find_all()

    assert response["webhook_endpoints"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_webhook_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.webhook_endpoints.find_all()


def test_valid_find_webhook_endpoint_request_with_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_standard_webhooks_response(),
    )
    response = client.webhook_endpoints.find(arg)

    assert response.signature_algo == "standard_webhooks"
    assert_standard_webhooks_signing_keys(response.signing_keys)


def test_valid_update_webhook_endpoint_request_with_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_standard_webhooks_response(),
    )
    response = client.webhook_endpoints.update(webhook_endpoint_object(), arg)

    assert_standard_webhooks_signing_keys(response.signing_keys)


def test_valid_create_standard_webhooks_endpoint_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        content=mock_standard_webhooks_response(),
    )
    response = client.webhook_endpoints.create(
        WebhookEndpoint(
            webhook_url="https://foo.bar",
            signature_algo="standard_webhooks",
            name="My Webhook Endpoint",
            event_types=["customer.created"],
        )
    )

    request_body = json.loads(httpx_mock.get_request().content)
    assert request_body["webhook_endpoint"]["signature_algo"] == "standard_webhooks"
    assert response.signature_algo == "standard_webhooks"
    assert_standard_webhooks_signing_keys(response.signing_keys)


def test_valid_find_webhook_endpoint_request_with_empty_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_empty_signing_keys_response(),
    )
    response = client.webhook_endpoints.find(arg)

    assert response.signing_keys == []


def test_valid_find_webhook_endpoint_request_without_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    arg = "b7ab2926-1de8-4428-9bcd-779314ac129b"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints/" + arg,
        content=mock_response(),
    )
    response = client.webhook_endpoints.find(arg)

    assert response.signing_keys is None


def test_valid_find_all_webhook_endpoint_request_without_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        content=mock_collection_response(),
    )
    response = client.webhook_endpoints.find_all()

    assert len(response["webhook_endpoints"]) > 0
    assert all(endpoint.signing_keys is None for endpoint in response["webhook_endpoints"])


def test_valid_find_all_webhook_endpoint_request_with_signing_keys(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/webhook_endpoints",
        content=mock_collection_standard_webhooks_response(),
    )
    response = client.webhook_endpoints.find_all()

    endpoints = response["webhook_endpoints"]
    assert len(endpoints) == 2
    assert endpoints[0].signature_algo == "standard_webhooks"
    assert_standard_webhooks_signing_keys(endpoints[0].signing_keys)
    assert endpoints[1].signing_keys == []
    assert response["meta"]["current_page"] == 1
