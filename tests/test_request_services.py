"""Test request services."""
import requests

from lago_python_client.services.request import make_url, send_delete_request, send_get_request, send_post_request, send_put_request


def test_make_url():
    """Make url."""
    # Given
    api_url = 'https://api.getlago.com/api/v1/'
    some_path_parts = ('team', 'anhtho', 'congratulate')
    query_name_value = {
        'message': "The future belongs to those who believe in the beauty of their dreams. Happy International Women's Day!",
        'date': '08.03.2023',
    }

    # When service is applied
    result = make_url(origin=api_url, path_parts=some_path_parts, query_pairs=query_name_value)
    # Then
    assert result == 'https://api.getlago.com/api/v1/team/anhtho/congratulate?message=The+future+belongs+to+those+who+believe+in+the+beauty+of+their+dreams.+Happy+International+Women%27s+Day%21&date=08.03.2023'


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
    """Ensure `send_delete_request` service use requests."""
    assert send_delete_request == requests.delete


def test_send_get_request():
    """Ensure `send_get_request` service use requests."""
    assert send_get_request == requests.get


def test_send_post_request():
    """Ensure `send_post_request` service use requests."""
    assert send_post_request == requests.post


def test_send_put_request():
    """Ensure `send_put_request` service use requests."""
    assert send_put_request == requests.put
