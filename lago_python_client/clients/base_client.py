from lago_python_client.models.base_model import BaseModel
from typing import Dict

import requests
import json


class BaseClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def create(self, input_object: BaseModel):
        _query_url = self.base_url + self.api_resource()
        _query_parameters = {
            self.root_name(): input_object.to_dict()
        }
        data = json.dumps(_query_parameters)
        requests.post(_query_url, data=data, headers=self.headers())

    def delete(self, params: Dict):
        _query_url = self.base_url + self.api_resource()
        _query_parameters = {
            self.root_name(): params
        }
        data = json.dumps(_query_parameters)
        requests.delete(_query_url, data=data, headers=self.headers())

    def headers(self):
        bearer = "Bearer " + self.api_key
        headers = {'Content-type': 'application/json', 'Authorization': bearer}

        return headers
