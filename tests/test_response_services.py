"""Test response services."""
from copy import deepcopy

from pydantic import BaseModel
import pytest
from httpx import Request, Response

from lago_python_client.exceptions import LagoApiError
from lago_python_client.services.response import (
    Response as ServiceResponse,
    RESPONSE_SUCCESS_CODES, _is_status_code_successful, _is_content_exists, verify_response,
    get_response_data, prepare_object_list_response, prepare_index_response, prepare_object_response,
)


def test_Response():
    """Ensure Response object is the same as ``request.Response``."""
    assert ServiceResponse == Response


def test_success_status_codes_exists():
    """Ensure ``RESPONSE_SUCCESS_CODES`` is set."""
    assert len(RESPONSE_SUCCESS_CODES) >= 4


def test_is_status_code_successful():
    """Check status code is successful."""
    # Given instanse of ``httpx.Response`` class with successful status code
    response = Response(content=b'{"a":{"b":"c"}}', status_code=200)
    # ... and with error status code
    response404 = deepcopy(response)
    response404._content = b''
    response404.status_code = 404

    # When check helper function is applied
    # Then verification passes.
    assert _is_status_code_successful(response) is True
    # ... or not
    assert _is_status_code_successful(response404) is False


def test_is_content_exists():
    """Check content exists."""
    # Given instanse of ``httpx.Response`` class with content
    response = Response(content=b'{"a":{"b":"c"}}', status_code=200)
    # ... and with empty content
    response204 = deepcopy(response)
    response204._content = b''
    response204.status_code = 204

    # When check helper function is applied
    # Then verification passes.
    assert _is_content_exists(response) is True
    # ... or not
    assert _is_content_exists(response204) is False


def test_verify_response():
    """Verify response."""
    # Given instanse of ``httpx.Response`` class with successful status code and content
    response = Response(content=b'{"a":{"b":"c"}}', status_code=200)
    # ... and with successful status code and empty content
    response204 = deepcopy(response)
    response204._content = b''
    response204.status_code = 204
    # ... and with error status code
    response404 = deepcopy(response)
    response404.status_code = 404
    response404.request = Request(method='POST', url='')

    # When service is applied
    # Then
    assert verify_response(response) == response
    assert verify_response(response204) is None
    with pytest.raises(LagoApiError):
        verify_response(response404)


def test_get_response_data():
    """Get response data."""
    # Given instanse of ``httpx.Response`` class with successful status code and content
    response = Response(content=b'{"a":{"b":"c"}}', status_code=200)
    # ... and with successful status code and content with sequence inside
    response200_2 = deepcopy(response)
    response200_2._content = b'[{"a": "b"}]'
    # ... and with successful status code and empty content
    response204 = deepcopy(response)
    response204._content = b''
    response204.status_code = 204
    # ... and with error status code
    response404 = deepcopy(response)
    response404.status_code = 404
    response404.request = Request(method='POST', url='')

    # When service is applied
    # Then
    assert get_response_data(response=response) == {
        'a': {
            'b': 'c',
        },
    }
    assert get_response_data(response=response, key='a') == {
        'b': 'c',
    }
    assert get_response_data(response=response200_2) == [
        {
            'a': 'b',
        },
    ]
    assert get_response_data(response=response204) is None
    with pytest.raises(LagoApiError):
        get_response_data(response=response404)


class SomeHumanModel(BaseModel):
    name: str


def test_prepare_object_response():
    """Verify ``prepare_object_response`` service returns Pydantic model instance."""
    # Given Pydantic model and some data
    data = {'name': 'Aurelia'}

    # When service is applied
    result = prepare_object_response(response_model=SomeHumanModel, data=data)
    # Then
    assert SomeHumanModel(**data) == result


def test_prepare_index_response():
    """Verify ``prepare_index_response`` service returns valid mapping object."""
    # Given Pydantic model and some data
    data = {
        'human': [
            {'name': 'Aurelia'},
            {'name': 'Aleksandra'},
            {'name': 'John'},
        ],
        'meta': {
            'something': 'is here'
        },
    }

    # When service is applied
    result = prepare_index_response(api_resource='human', response_model=SomeHumanModel, data=data)
    # Then
    assert SomeHumanModel(**data['human'][0]) in result['human']
    assert len(result['human']) == 3
    assert 'meta' in result


def test_prepare_object_list_response():
    """Verify ``prepare_object_list_response`` service returns valid mapping object."""
    # Given Pydantic model and some data
    data = [
        {'name': 'Aurelia'},
        {'name': 'Aleksandra'},
        {'name': 'John'},
    ]

    # When service is applied
    result = prepare_object_list_response(api_resource='human', response_model=SomeHumanModel, data=data)
    # Then
    assert SomeHumanModel(**data[0]) == result['human'][0]
    assert len(result['human']) == 3
