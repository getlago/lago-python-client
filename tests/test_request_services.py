"""Test request services."""
import httpx

from lago_python_client.services.request import make_headers, make_url, send_delete_request, send_get_request, send_post_request, send_put_request
from lago_python_client.version import LAGO_VERSION


def test_make_headers():
    """Make headers."""
    # Give api_key
    api_key: str = "test"
    # When service is applied
    result = make_headers(api_key=api_key)
    # Then
    assert result == {
        'Content-type': 'application/json',
        'Authorization': "Bearer test",
        'User-agent': 'Lago Python v{version}'.format(version=LAGO_VERSION),
    }


def test_make_url():
    """Make url."""
    # Given
    api_url = 'https://api.getlago.com/api/v1/'
    some_path_parts = ('team', 'anhtho', 'congratulate')
    query_name_value = {
        'message': "The future belongs to those who believe in the beauty of their dreams. Happy International Women's Day!",
        'day': 8,
    }

    # When service is applied
    result = make_url(origin=api_url, path_parts=some_path_parts, query_pairs=query_name_value)
    # Then
    assert result == 'https://api.getlago.com/api/v1/team/anhtho/congratulate?message=The+future+belongs+to+those+who+believe+in+the+beauty+of+their+dreams.+Happy+International+Women%27s+Day%21&day=8'


def test_make_url_no_query():
    """Make url without query name-value pairs."""
    # Given
    api_url = 'https://api.getlago.com/api/v1/'
    some_path_parts = ('hello', )

    # When service is applied
    result = make_url(origin=api_url, path_parts=some_path_parts)
    # Then
    assert result == 'https://api.getlago.com/api/v1/hello'


def test_send_delete_request():
    """Ensure `send_delete_request` service use httpx."""
    assert send_delete_request == httpx.delete


def test_send_get_request():
    """Ensure `send_get_request` service use httpx."""
    assert send_get_request == httpx.get


def test_send_post_request():
    """Ensure `send_post_request` service use httpx."""
    assert send_post_request == httpx.post


def test_send_put_request():
    """Ensure `send_put_request` service use httpx."""
    assert send_put_request == httpx.put
