"""Test request services."""

import pytest

from lago_python_client.services.request import (
    make_headers,
    make_url,
    send_delete_request,
    send_get_request,
    send_post_request,
    send_put_request,
)
from lago_python_client.version import LAGO_VERSION


@pytest.mark.parametrize(
    "identifier,encoded",
    [
        ("customer#billing", "customer%23billing"),
        ("customer?expand=all", "customer%3Fexpand%3Dall"),
        ("tenant/customer", "tenant%2Fcustomer"),
        ("customer%2Fbilling", "customer%252Fbilling"),
        ("customer name", "customer%20name"),
        ("客戶", "%E5%AE%A2%E6%88%B6"),
        ("..", "%2E%2E"),
        (".", "%2E"),
    ],
)
def test_make_url_treats_identifiers_as_path_segments(identifier, encoded):
    assert make_url(
        origin="https://api.getlago.com/api/v1/",
        path_parts=("customers", identifier, "current_usage"),
        query_pairs={"external_subscription_id": "sub#1"},
    ) == (f"https://api.getlago.com/api/v1/customers/{encoded}/current_usage?external_subscription_id=sub%231")


def test_make_headers():
    """Make headers."""
    # Give api_key
    api_key: str = "test"
    # When service is applied
    result = make_headers(api_key=api_key)
    # Then
    assert result == {
        "Content-type": "application/json",
        "Authorization": "Bearer test",
        "User-agent": f"Lago Python v{LAGO_VERSION}",
    }


def test_make_url():
    """Make url."""
    # Given
    api_url = "https://api.getlago.com/api/v1/"
    some_path_parts = ("team", "anhtho", "congratulate")
    query_name_value = {
        "message": "The future belongs to those who believe in the beauty of their dreams. Happy International Women's Day!",
        "day": 8,
    }

    # When service is applied
    result = make_url(origin=api_url, path_parts=some_path_parts, query_pairs=query_name_value)
    # Then
    assert (
        result
        == "https://api.getlago.com/api/v1/team/anhtho/congratulate?message=The+future+belongs+to+those+who+believe+in+the+beauty+of+their+dreams.+Happy+International+Women%27s+Day%21&day=8"
    )


def test_make_url_no_query():
    """Make url without query name-value pairs."""
    # Given
    api_url = "https://api.getlago.com/api/v1/"
    some_path_parts = ("hello",)

    # When service is applied
    result = make_url(origin=api_url, path_parts=some_path_parts)
    # Then
    assert result == "https://api.getlago.com/api/v1/hello"


def test_send_delete_request():
    """Ensure `send_delete_request` is a callable wrapper."""
    assert callable(send_delete_request)


def test_send_get_request():
    """Ensure `send_get_request` is a callable wrapper."""
    assert callable(send_get_request)


def test_send_post_request():
    """Ensure `send_post_request` is a callable wrapper."""
    assert callable(send_post_request)


def test_send_put_request():
    """Ensure `send_put_request` is a callable wrapper."""
    assert callable(send_put_request)


def test_make_url_with_list_query_params():
    base_url = "http://example.com"
    url = make_url(origin=base_url, path_parts=("test",), query_pairs={"status[]": ["active", "terminated"]})
    assert url == "http://example.com/test?status%5B%5D=active&status%5B%5D=terminated"

    url = make_url(
        origin=base_url, path_parts=("test",), query_pairs=(("status[]", "active"), ("status[]", "terminated"))
    )
    assert url == "http://example.com/test?status%5B%5D=active&status%5B%5D=terminated"
