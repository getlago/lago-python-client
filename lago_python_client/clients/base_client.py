import requests
import json

from pydantic import BaseModel
from requests import Response
from typing import Dict
from urllib.parse import urljoin, urlencode
from lago_python_client.version import LAGO_VERSION


class BaseClient:
    RESPONSE_SUCCESS_CODES = [200, 201, 202, 204]

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def find(self, resource_id: str, params: Dict = None):
        api_resource = self.api_resource() + '/' + resource_id
        query_url = urljoin(self.base_url, api_resource)

        data = None
        if params is not None:
            data = json.dumps(params)

        api_response = requests.get(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)

    def find_all(self, options: Dict = None):
        if options:
            api_resource = self.api_resource() + '?' + urlencode(options)
        else:
            api_resource = self.api_resource()

        query_url = urljoin(self.base_url, api_resource)

        api_response = requests.get(query_url, headers=self.headers())
        data = self.handle_response(api_response).json()

        return self.prepare_index_response(data)

    def destroy(self, resource_id: str):
        api_resource = self.api_resource() + '/' + resource_id
        query_url = urljoin(self.base_url, api_resource)

        api_response = requests.delete(query_url, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)

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

    def update(self, input_object: BaseModel, identifier: str = None):
        api_resource = self.api_resource()

        if identifier is not None:
            api_resource = api_resource + '/' + identifier

        query_url = urljoin(self.base_url, api_resource)
        query_parameters = {
            self.root_name(): input_object.dict(exclude_none=True)
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

    def prepare_index_response(self, data: Dict):
        collection = []

        for el in data[self.api_resource()]:
            collection.append(self.prepare_response(el))

        response = {
            self.api_resource(): collection,
            'meta': data['meta']
        }

        return response


class LagoApiError(Exception):
    ...
