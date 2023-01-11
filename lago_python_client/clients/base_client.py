from collections.abc import MutableMapping
import json
from http import HTTPStatus
from typing import Any, Optional
from urllib.parse import urljoin, urlencode

import orjson
from pydantic import BaseModel
import requests
from requests import Response

from lago_python_client.version import LAGO_VERSION


class BaseClient:
    RESPONSE_SUCCESS_CODES = [200, 201, 202, 204]

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def find(self, resource_id: str, params: Optional[dict] = None):
        api_resource = self.api_resource() + '/' + resource_id
        query_url = urljoin(self.base_url, api_resource)

        data = None
        if params is not None:
            data = json.dumps(params)

        api_response = requests.get(query_url, data=data, headers=self.headers())
        data = self.handle_response(api_response).json().get(self.root_name())

        return self.prepare_response(data)

    def find_all(self, options: Optional[dict] = None):
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

    def update(self, input_object: BaseModel, identifier: Optional[str] = None):
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

    def handle_response(self, response: Response) -> Optional[Response]:
        if response.status_code in BaseClient.RESPONSE_SUCCESS_CODES:
            if response.text:
                return response
            else:
                return None
        else:
            if response.text:
                response_data: Any = orjson.loads(response.text)
                detail: Optional[str] = getattr(response_data, 'error', None)
            else:
                response_data = None
                detail = None
            raise LagoApiError(
                status_code=response.status_code,
                url=response.request.url,
                response=response_data,
                detail=detail,
                headers=response.headers,
            )

    def prepare_index_response(self, data: dict):
        collection = []

        for el in data[self.api_resource()]:
            collection.append(self.prepare_response(el))

        response = {
            self.api_resource(): collection,
            'meta': data['meta']
        }

        return response


class LagoApiError(Exception):
    def __init__(
        self,
        status_code: int,
        url: Optional[str],
        response: Any,
        detail: Optional[str] = None,
        headers: Optional[MutableMapping[str, str]] = None,
    ) -> None:
        if detail is None:
            detail = HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.url = url
        self.response = response
        self.detail = detail
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
