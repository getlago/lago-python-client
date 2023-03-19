from abc import ABC, abstractmethod
import sys
from typing import Any, Optional, Type, Union

from pydantic import BaseModel
import requests
from requests import Response

from ..services.json import to_json
from ..services.request import make_url
from ..services.response import get_response_data, prepare_index_response, prepare_object_response
from ..version import LAGO_VERSION

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class BaseClient(ABC):
    """The base class used for each collection client."""

    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    @property
    @classmethod
    @abstractmethod
    def API_RESOURCE(cls) -> str:
        """Collection name (required class property) used to build query urls."""
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def RESPONSE_MODEL(cls) -> Type[BaseModel]:
        """Response model (required class property) used to prepare response."""
        raise NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def ROOT_NAME(cls) -> str:
        """The resource key (required class property), used to access the response data."""
        raise NotImplementedError

    def find(self, resource_id: str, params: Mapping[str, str] = {}) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id),
        )
        data = to_json(params) if params else None

        api_response: Response = requests.get(query_url, data=data, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def find_all(self, options: Mapping[str, str] = {}) -> Mapping[str, Any]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
            query_pairs=options,
        )
        api_response: Response = requests.get(query_url, headers=self.headers())

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )

    def destroy(self, resource_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id),
        )
        api_response: Response = requests.delete(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def create(self, input_object: BaseModel) -> Union[Optional[BaseModel], bool]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
        )
        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        api_response: Response = requests.post(query_url, data=to_json(query_parameters), headers=self.headers())

        if not (response_data := get_response_data(response=api_response, key=self.ROOT_NAME)):
            return True  # TODO: should return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )

    def update(self, input_object: BaseModel, identifier: Optional[str] = None) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, identifier) if identifier else (self.API_RESOURCE, ),
        )
        query_parameters = {
            self.ROOT_NAME: input_object.dict(exclude_none=True)
        }
        data = to_json(query_parameters)
        api_response: Response = requests.put(query_url, data=data, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def headers(self) -> Mapping[str, str]:
        bearer = "Bearer " + self.api_key
        user_agent = 'Lago Python v' + LAGO_VERSION
        headers = {
            'Content-type': 'application/json',
            'Authorization': bearer,
            'User-agent': user_agent
        }

        return headers
