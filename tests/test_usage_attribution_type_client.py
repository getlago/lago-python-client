import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.usage_attribution_type import UsageAttributionType


def usage_attribution_type_object():
    return UsageAttributionType(
        code="team",
        name="Team",
        description="Teams of the customer",
        role="hierarchical",
        parent_code="department",
        attribution_keys=["team_id"],
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/usage_attribution_type.json")

    with open(data_path, "rb") as usage_attribution_type_response:
        return usage_attribution_type_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/usage_attribution_type_index.json")

    with open(data_path, "rb") as usage_attribution_type_response:
        return usage_attribution_type_response.read()


def test_valid_create_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/usage_attribution_types",
        content=mock_response(),
    )
    response = client.usage_attribution_types.create(usage_attribution_type_object())

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.code == "team"
    assert response.attribution_keys == ["team_id"]
    assert response.role == "hierarchical"
    assert response.lago_parent_id == "1a901a90-1a90-1a90-1a90-1a901a901a92"
    assert response.parent_code == "department"


def test_invalid_create_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/usage_attribution_types",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.usage_attribution_types.create(usage_attribution_type_object())


def test_valid_update_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "team"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        content=mock_response(),
    )
    response = client.usage_attribution_types.update(usage_attribution_type_object(), code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.code == code


def test_invalid_update_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.usage_attribution_types.update(usage_attribution_type_object(), code)


def test_valid_find_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "team"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        content=mock_response(),
    )
    response = client.usage_attribution_types.find(code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.code == code


def test_invalid_find_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.usage_attribution_types.find(code)


def test_valid_destroy_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "team"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        content=mock_response(),
    )
    response = client.usage_attribution_types.destroy(code)

    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.code == code


def test_invalid_destroy_usage_attribution_type_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/usage_attribution_types/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.usage_attribution_types.destroy(code)


def test_valid_find_all_usage_attribution_types_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/usage_attribution_types",
        content=mock_collection_response(),
    )
    response = client.usage_attribution_types.find_all()

    assert response["usage_attribution_types"][0].code == "department"
    assert response["usage_attribution_types"][1].role == "flat"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_usage_attribution_types_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/usage_attribution_types?per_page=2&page=1&role=flat&search_term=mod",
        content=mock_collection_response(),
    )
    response = client.usage_attribution_types.find_all({"per_page": 2, "page": 1, "role": "flat", "search_term": "mod"})

    assert response["usage_attribution_types"][1].code == "model"
    assert response["meta"]["total_count"] == 2


def test_invalid_find_all_usage_attribution_types_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/usage_attribution_types",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.usage_attribution_types.find_all()
