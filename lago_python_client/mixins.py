import sys
from typing import Any, Optional, Type, Union
try:
    from typing import Protocol
except ImportError:  # Python 3.7
    from typing_extensions import Protocol  # type: ignore

from pydantic import BaseModel
import requests
from requests import Response

from .services.json import to_json
from .services.request import make_url
from .services.response import get_response_data, prepare_index_response, prepare_object_response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class _ClientMixin(Protocol):
    @property
    def API_RESOURCE(self) -> str: ...
    @property
    def RESPONSE_MODEL(self) -> Type[BaseModel]: ...
    @property
    def ROOT_NAME(self) -> str: ...
    @property
    def api_key(self) -> str: ...
    @property
    def base_url(self) -> str: ...
    def headers(self) -> Mapping[str, str]: ...


class CreateCommandMixin:
    """Client mixin with `create` command."""

    def create(self: _ClientMixin, input_object: BaseModel) -> Union[Optional[BaseModel], bool]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
        )
        query_parameters = {
            self.ROOT_NAME: input_object.dict()
        }
        api_response: Response = requests.post(query_url, data=to_json(query_parameters), headers=self.headers())

        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return True  # TODO: should return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )


class DestroyCommandMixin:
    """Client mixin with `destroy` command."""

    def destroy(self: _ClientMixin, resource_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, resource_id),
        )
        api_response: Response = requests.delete(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class FindAllCommandMixin:
    """Client mixin with `find_all` command."""

    def find_all(self: _ClientMixin, options: Mapping[str, str] = {}) -> Mapping[str, Any]:
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


class FindCommandMixin:
    """Client mixin with `find` command."""

    def find(self: _ClientMixin, resource_id: str, params: Mapping[str, str] = {}) -> BaseModel:
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


class UpdateCommandMixin:
    """Client mixin with `update` command."""

    def update(self: _ClientMixin, input_object: BaseModel, identifier: Optional[str] = None) -> BaseModel:
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
