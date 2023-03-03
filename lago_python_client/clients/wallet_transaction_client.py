import requests

from .base_client import BaseClient
from pydantic import BaseModel
from requests import Response
from lago_python_client.models.wallet_transaction import WalletTransactionResponse
from urllib.parse import urljoin, urlencode
from ..services.json import from_json, to_json
from ..services.response import verify_response


class WalletTransactionClient(BaseClient):
    def api_resource(self):
        return 'wallet_transactions'

    def root_name(self):
        return 'wallet_transactions'

    def create(self, input_object: BaseModel):
        query_url = urljoin(self.base_url, self.api_resource())
        query_parameters = {
            'wallet_transaction': input_object.dict()
        }
        data = to_json(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        data = verify_response(api_response)

        return self.prepare_response(from_json(data).get(self.root_name()))

    def find_all(self, wallet_id: str, options: dict = {}):
        if options:
            api_resource = 'wallets/' + wallet_id + '/wallet_transactions?' + urlencode(options)
        else:
            api_resource = 'wallets/' + wallet_id + '/wallet_transactions'

        query_url = urljoin(self.base_url, api_resource)
        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)

    def prepare_object_response(self, data: dict):
        return WalletTransactionResponse.parse_obj(data)

    def prepare_response(self, data):
        collection = []

        for el in data:
            collection.append(self.prepare_object_response(el))

        response = {
            self.api_resource(): collection
        }

        return response

    def prepare_index_response(self, data: dict):
        collection = []

        for el in data[self.api_resource()]:
            collection.append(self.prepare_object_response(el))

        response = {
            self.api_resource(): collection,
            'meta': data['meta']
        }

        return response
