from abc import ABC, abstractmethod
from typing import Any, Optional
from urllib.parse import urljoin, urlencode

from pydantic import BaseModel
import requests
from requests import Response

from ..services.json import from_json, to_json
from ..services.response import verify_response
from ..version import LAGO_VERSION


class BaseClient(ABC):
    """The base class used for each collection client."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    @property  # type: ignore
    @classmethod
    @abstractmethod
    def API_RESOURCE(cls) -> str:
        """Collection name (required class property) used to build query urls."""
        raise NotImplementedError

    @property  # type: ignore
    @classmethod
    @abstractmethod
    def ROOT_NAME(cls) -> str:
        """The resource key (required class property), used to access the response data."""
        raise NotImplementedError

    def find(self, resource_id: str, params: dict = {}):
        uri: str = '/'.join((self.API_RESOURCE, resource_id))
        query_url: str = urljoin(self.base_url, uri)

        data = to_json(params) if params else None

        api_response = requests.get(query_url, data=data, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_response(data)

    def find_all(self, options: dict = {}):
        uri: str = '{uri_path}{uri_query}'.format(
            uri_path=self.API_RESOURCE,
            uri_query=f'?{urlencode(options)}' if options else '',
        )
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)

    def destroy(self, resource_id: str):
        uri: str = '/'.join((self.API_RESOURCE, resource_id))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.delete(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_response(data)

    def create(self, input_object: BaseModel):
        query_url: str = urljoin(self.base_url, self.API_RESOURCE)

        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        data = to_json(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True
        else:
            return self.prepare_response(from_json(data).get(self.ROOT_NAME))

    def update(self, input_object: BaseModel, identifier: Optional[str] = None):
        uri: str = '/'.join((self.API_RESOURCE, identifier)) if identifier else self.API_RESOURCE
        query_url: str = urljoin(self.base_url, uri)

        query_parameters = {
            self.ROOT_NAME: input_object.dict(exclude_none=True)
        }
        data = to_json(query_parameters)
        api_response = requests.put(query_url, data=data, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

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

    def prepare_index_response(self, data: dict):
        collection = []

        for el in data[self.API_RESOURCE]:
            collection.append(self.prepare_response(el))

        response = {
            self.API_RESOURCE: collection,
            'meta': data['meta']
        }

        return response
