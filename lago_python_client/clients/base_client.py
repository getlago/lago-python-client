import requests
import json

from lago_python_client.models.base_model import BaseModel
from requests import Response
from typing import Dict
from urllib.parse import urljoin


def handle_response(response: Response):
    if response.status_code in BaseClient.RESPONSE_SUCCESS_CODES:
        if response.text:
            return response.json()
        else:
            return None
    else:
        raise LagoApiError(
            "URI: %s. Status code: %s. Response: %s." % (
                response.request.url, response.status_code, response.text)
        )


class BaseClient:
    RESPONSE_SUCCESS_CODES = [200, 201, 202, 204]

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def create(self, input_object: BaseModel):
        _query_url = urljoin(self.base_url, self.api_resource())
        _query_parameters = {
            self.root_name(): input_object.to_dict()
        }
        data = json.dumps(_query_parameters)
        api_response = requests.post(_query_url, data=data, headers=self.headers())
        data = handle_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(data.get(self.root_name()))  # Customer.parse_obj(data) / Customer.dict()

    def delete(self, params: Dict):
        _query_url = urljoin(self.base_url, self.api_resource())
        data = json.dumps(params)
        api_response = requests.delete(_query_url, data=data, headers=self.headers())
        data = handle_response(api_response).get(self.root_name())

        return self.prepare_response(data)

    def headers(self):
        bearer = "Bearer " + self.api_key
        headers = {'Content-type': 'application/json', 'Authorization': bearer}

        return headers


class LagoApiError(Exception):
    ...
