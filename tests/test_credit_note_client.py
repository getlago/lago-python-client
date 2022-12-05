import unittest
import requests_mock
import os

from lago_python_client.client import Client
from lago_python_client.models.invoice import FeeResponse
from lago_python_client.models.credit_note import Item, Items, CreditNote, CreditNoteUpdate
from lago_python_client.clients.base_client import LagoApiError

def credit_note_object():
    item1 = Item(
        fee_id="fee_id_1",
        credit_amount_cents=10,
        refund_amount_cents=10,
    )

    item2 = Item(
        fee="fee_id_2",
        credit_amount_cents=5,
        refund_amount_cents=5,
    )

    return CreditNote(
        lago_id="credit_note_id",
        reason= 'other',
        items= Items(__root__=[item1, item2])
    )

def credit_note_update_object():
    return CreditNoteUpdate(refund_status='pending')

def mock_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/credit_note.json')

    with open(data_path, 'r') as credit_note_response:
        return credit_note_response.read()

def mock_collection_response():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'fixtures/credit_note_index.json')

    with open(data_path, 'r') as credit_notes_response:
        return credit_notes_response.read()

class TestCreditNoteClient(unittest.TestCase):
    def test_valid_find_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/credit_notes/' + identifier, text=mock_response())
            response = client.credit_notes().find(identifier)

        self.assertEqual(response.lago_id, identifier)

    def test_invalid_find_invoice_request(self):
        client = Client(api_key='invalid')
        identifier = '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba'

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/credit_notes/' + identifier, status_code=404, text='')

        with self.assertRaises(LagoApiError):
            client.credit_notes().find(identifier)

    def test_valid_find_all_credit_notes_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('GET', 'https://api.getlago.com/api/v1/credit_notes', text=mock_collection_response())
            response = client.credit_notes().find_all({'per_page': 2, 'page': 1})

        self.assertEqual(response['credit_notes'][0].lago_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')
        self.assertEqual(response['meta']['current_page'], 1)

    def test_valid_download_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST',
                            'https://api.getlago.com/api/v1/credit_notes/5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba/download',
                            text=mock_response())
            response = client.credit_notes().download('5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

        self.assertEqual(response.lago_id, '5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba')

    def test_valid_create_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/credit_notes', text=mock_response())
            response = client.credit_notes().create(credit_note_object())

        self.assertEqual(response.lago_id, "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba")
        self.assertEqual(response.refund_status, 'pending')

    def test_invalid_create_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')

        with requests_mock.Mocker() as m:
            m.register_uri('POST', 'https://api.getlago.com/api/v1/credit_notes', status_code=422, text='')

            with self.assertRaises(LagoApiError):
                client.credit_notes().create(credit_note_object())

    def test_valid_update_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        credit_note_id = 'credit-note-id'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/credit_notes/' + credit_note_id,
                           text=mock_response())
            response = client.credit_notes().update(credit_note_update_object(), credit_note_id)

        self.assertEqual(response.lago_id, "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba")
        self.assertEqual(response.refund_status, 'pending')

    def test_valid_void_credit_note_request(self):
        client = Client(api_key='886fe239-927d-4072-ab72-6dd345e8dd0d')
        credit_note_id = 'credit-note-id'

        with requests_mock.Mocker() as m:
            m.register_uri('PUT',
                           'https://api.getlago.com/api/v1/credit_notes/' + credit_note_id + '/void',
                           text=mock_response())
            response = client.credit_notes().void(credit_note_id)

        self.assertEqual(response.lago_id, "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba")
        self.assertEqual(response.refund_status, 'pending')

if __name__ == '__main__':
    unittest.main()
