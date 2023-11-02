import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models.fee import FeeResponse
from lago_python_client.models.credit_note import Item, Items, CreditNote, CreditNoteUpdate, CreditNoteEstimate


def credit_note_object():
    item1 = Item(
        fee_id="fee_id_1",
        amount_cents=10
    )

    item2 = Item(
        fee="fee_id_2",
        amount_cents=5
    )

    return CreditNote(
        lago_id="credit_note_id",
        reason= 'other',
        items= Items(__root__=[item1, item2])
    )


def credit_note_update_object():
    return CreditNoteUpdate(refund_status='pending')


def estimate_credit_note():
    item1 = Item(
        fee_id="fee_id_1",
        amount_cents=10,
    )

    item2 = Item(
        fee="fee_id_2",
        amount_cents=5,
    )

    return CreditNoteEstimate(
        invoice_id='1a901a90-1a90-1a90-1a90-1a901a901a90',
        items= Items(__root__=[item1, item2])
    )


def mock_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/credit_note.json')

    with open(data_path, 'rb') as credit_note_response:
        return credit_note_response.read()


def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/credit_note_index.json')

    with open(data_path, 'rb') as credit_notes_response:
        return credit_notes_response.read()


def mock_estimated_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/credit_note_estimated.json')

    with open(data_path, 'rb') as credit_note_estimated_response:
        return credit_note_estimated_response.read()


def test_valid_find_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/credit_notes/' + identifier, content=mock_response())
    response = client.credit_notes.find(identifier)

    assert response.lago_id == identifier


def test_invalid_find_invoice_request(httpx_mock: HTTPXMock):
    client = Client(api_key='invalid')
    identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/credit_notes/' + identifier, status_code=404, content=b'')

    with pytest.raises(LagoApiError):
        client.credit_notes.find(identifier)


def test_valid_find_all_credit_notes_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='GET', url='https://api.getlago.com/api/v1/credit_notes?per_page=2&page=1', content=mock_collection_response())
    response = client.credit_notes.find_all({'per_page': 2, 'page': 1})

    assert response['credit_notes'][0].lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'
    assert response['meta']['current_page'] == 1


def test_valid_download_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(
        method='POST',
        url='https://api.getlago.com/api/v1/credit_notes/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/download',
        content=mock_response(),
    )
    response = client.credit_notes.download('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    assert response.lago_id == '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'


def test_valid_create_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/credit_notes', content=mock_response())
    response = client.credit_notes.create(credit_note_object())

    assert response.lago_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.refund_status == 'pending'


def test_invalid_create_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/credit_notes', status_code=422, content=b'')

    with pytest.raises(LagoApiError):
        client.credit_notes.create(credit_note_object())


def test_valid_update_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    credit_note_id = 'credit-note-id'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/credit_notes/' + credit_note_id, content=mock_response())
    response = client.credit_notes.update(credit_note_update_object(), credit_note_id)

    assert response.lago_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.refund_status == 'pending'


def test_valid_void_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
    credit_note_id = 'credit-note-id'

    httpx_mock.add_response(method='PUT', url='https://api.getlago.com/api/v1/credit_notes/' + credit_note_id + '/void', content=mock_response())
    response = client.credit_notes.void(credit_note_id)

    assert response.lago_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.refund_status == 'pending'


def test_valid_estimate_credit_note_request(httpx_mock: HTTPXMock):
    client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

    httpx_mock.add_response(method='POST', url='https://api.getlago.com/api/v1/credit_notes/estimate', content=mock_estimated_response())
    response = client.credit_notes.estimate(estimate_credit_note())

    assert response.lago_invoice_id == '1a901a90-1a90-1a90-1a90-1a901a901a90'
