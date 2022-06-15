import requests
import json

from pydantic import BaseModel
from requests import Response
from typing import Dict
from urllib.parse import urljoin
from lago_python_client.version import LAGO_VERSION


class BaseClient:
    RESPONSE_SUCCESS_CODES = [200, 201, 202, 204]

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def create(self, input_object: BaseModel):
        query_url = urljoin(self.base_url, self.api_resource())
        query_parameters = {
            self.root_name(): input_object.dict()
        }
        data = json.dumps(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(data.json().get(self.root_name()))

    def delete(self, params: Dict):
        query_url = urljoin(self.base_url, self.api_resource())
        data = json.dumps(params)
        api_response = requests.delete(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)

    def update(self, input_object: BaseModel):
        api_resource = self.api_resource() + '/' + input_object.lago_id
        query_url = urljoin(self.base_url, api_resource)

        payload = input_object.dict()
        payload.pop('lago_id', None)

        query_parameters = {
            self.root_name(): payload
        }
        data = json.dumps(query_parameters)
        api_response = requests.put(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)

    def headers(self):
        bearer = "Bearer " + self.api_key
        user_agent = 'Lago Python v' + LAGO_VERSION
        headers = {
            'Content-type': 'application/json',
            'Authorization': bearer,
            'User-agent': user_agent
        }

        return headers

    def handle_response(self, response: Response):
        if response.status_code in BaseClient.RESPONSE_SUCCESS_CODES:
            if response.text:
                return response
            else:
                return None
        else:
            raise LagoApiError(
                "URI: %s. Status code: %s. Response: %s." % (
                    response.request.url, response.status_code, response.text)
            )


class LagoApiError(Exception):
    ...
