import requests
import json

from .base_client import BaseClient
from pydantic import BaseModel
from requests import Response
from lago_python_client.models.wallet_transaction import WalletTransactionResponse
from typing import Dict
from urllib.parse import urljoin, urlencode


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
        data = json.dumps(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response)

        return self.prepare_response(data.json().get(self.root_name()))

    def prepare_object_response(self, data: Dict):
        return WalletTransactionResponse.parse_obj(data)

    def prepare_response(self, data):
        collection = []

        for el in data:
            collection.append(self.prepare_object_response(el))

        response = {
            self.api_resource(): collection
        }

        return response
