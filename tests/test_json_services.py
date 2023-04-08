"""Test JSON services."""
from httpx import Response
import pytest

from lago_python_client.exceptions import LagoApiError
from lago_python_client.services.json import from_json, to_json


def test_from_json():
    """Deserialize data from json string."""
    # Given some data
    expected_data = {'a': {'b': 'c'}}
    # And same data serialized in json format stored as string,
    json_string = '{"a":{"b":"c"}}'
    # ... or bytes,
    json_bytes = b'{"a":{"b":"c"}}'
    # ... or even available as ``content`` property of instanse of ``httpx.Response`` class
    json_httpx_response = Response(content=json_bytes, status_code=200)
    # ... or None
    json_none = None
    # ... or something incorrect
    json_string_shit_happens = b'{"abc'

    # When service is applied
    # Then service result is equal to given data.
    assert from_json(json_string) == expected_data
    assert from_json(json_bytes) == expected_data
    assert from_json(json_httpx_response) == expected_data
    # ... or raise exception
    with pytest.raises(LagoApiError) as cm:
        from_json(json_none)
    assert cm.value.detail == 'Input must be bytes, bytearray, memoryview, or str'
    with pytest.raises(LagoApiError):
        from_json(json_string_shit_happens)


def test_to_json():
    """Serialize data to json bytestring."""
    # Given some data
    initial_data = {'a': {'b': 'c'}}
    # And same data serialized in json format
    expected_json_string = b'{"a":{"b":"c"}}'

    # When service is applied
    # Then service result is equal to given serialized json string.
    assert to_json(initial_data) == expected_json_string
