from abc import ABC, abstractmethod
from typing import Optional, Type

from pydantic import BaseModel
import requests
from requests import Response

from ..services.json import from_json, to_json
from ..services.request import make_url
from ..services.response import prepare_index_response, prepare_object_response, verify_response
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
    def RESPONSE_MODEL(cls) -> Type[BaseModel]:
        """Response model (required class property) used to prepare response."""
        raise NotImplementedError

    @property  # type: ignore
    @classmethod
    @abstractmethod
    def ROOT_NAME(cls) -> str:
        """The resource key (required class property), used to access the response data."""
        raise NotImplementedError

    def find(self, resource_id: str, params: dict = {}):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id),
        )
        data = to_json(params) if params else None

        api_response: Response = requests.get(query_url, data=data, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def find_all(self, options: dict = {}):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
            query_pairs=options,
        )
        api_response: Response = requests.get(query_url, headers=self.headers())

        return prepare_index_response(
            api_resourse=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)),
        )

    def destroy(self, resource_id: str):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id),
        )
        api_response: Response = requests.delete(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def create(self, input_object: BaseModel):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
        )
        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        data = to_json(query_parameters)
        api_response: Response = requests.post(query_url, data=data, headers=self.headers())
        data = verify_response(api_response)

        if data is None:
            return True

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(data).get(self.ROOT_NAME),
        )

    def update(self, input_object: BaseModel, identifier: Optional[str] = None):
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
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def headers(self):
        bearer = "Bearer " + self.api_key
        user_agent = 'Lago Python v' + LAGO_VERSION
        headers = {
            'Content-type': 'application/json',
            'Authorization': bearer,
            'User-agent': user_agent
        }

        return headers
