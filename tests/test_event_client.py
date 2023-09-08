import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.event import BatchEvent, Event


def create_event():
    return Event(external_customer_id='5eb02857-a71e-4ea2-bcf9-57d8885990ba', code='123', transaction_id='123')


def create_event_with_string_timestamp():
    return Event(external_customer_id='5eb02857-a71e-4ea2-bcf9-57d8885990ba', code='123', transaction_id='123', timestamp='1651240791.123')


def create_batch_event():
    return BatchEvent(external_subscription_ids=['88u02857-a71e-4ea2-bcf9-57d8885990ba'], code='123', transaction_id='123')


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/event.json')

    with open(data_path, 'rb') as event_response:
        return event_response.read()

def mock_fees_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, 'fixtures/fees.json')

    with open(data_path, 'rb') as fees_response:
        return fees_response.read()


def test_valid_create_events_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events', content=b'')
    client.events.create(create_event())  # Any response means success, any exception - failure


def test_valid_create_events_request_with_string_timestamp(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events', content=b'')
    client.events.create(create_event_with_string_timestamp())  # Any response means success, any exception - failure


def test_invalid_create_events_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.events.create(create_event())


def test_valid_create_batch_events_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events/batch', content=b'')
    client.events.batch_create(create_batch_event())  # Any response means success, any exception - failure


def test_invalid_create_batch_events_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events/batch', status_code=401, content=b'')

    with pytest.raises(LagoApiError):
        client.events.batch_create(create_batch_event())


def test_valid_find_event_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    event_id = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/events/' + event_id, content=mock_response())
    response = client.events.find(event_id)

    assert response.lago_id == event_id


def test_invalid_find_events_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    event_id = 'INVALID_EVENT'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/events/' + event_id, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.events.find(event_id)


def test_valid_estimate_fees_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events/estimate_fees', content=mock_fees_response())
    response = client.events.estimate_fees(create_event())

    assert response['fees'][0].item.type == 'instant_charge'


def test_invalid_estimate_fees_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/events/estimate_fees', status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.events.estimate_fees(create_event())
