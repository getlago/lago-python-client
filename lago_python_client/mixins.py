import sys
from typing import Any, Generic, Optional, Type, TypeVar, Union

import httpx

try:
    from typing import Protocol
except ImportError:  # Python 3.7
    from typing_extensions import Protocol  # type: ignore

from pydantic import BaseModel

from .services.json import to_json
from .services.request import make_headers, make_url, send_delete_request, send_get_request, send_post_request, send_put_request
from .services.response import get_response_data, prepare_index_response, prepare_object_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping

_PM = TypeVar("_PM", covariant=True)
_M = TypeVar("_M", bound=BaseModel)


class _ClientMixin(Protocol[_PM]):
    @property
    def API_RESOURCE(self) -> str: ...
    @property
    def RESPONSE_MODEL(self) -> Type[_PM]: ...
    @property
    def ROOT_NAME(self) -> str: ...
    @property
    def api_key(self) -> str: ...
    @property
    def base_url(self) -> str: ...


class CreateCommandMixin(Generic[_M]):
    """Client mixin with `create` command."""

    def create(self: _ClientMixin[_M], input_object: BaseModel, timeout: Optional[httpx.Timeout] = None) -> Optional[_M]:
        """Execute `create` command."""
        # Send request and save response
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, ),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(),
            }),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        response_data = get_response_data(response=api_response, key=self.ROOT_NAME)
        if not response_data:
            return None

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=response_data,
        )


class DestroyCommandMixin(Generic[_M]):
    """Client mixin with `destroy` command."""

    def destroy(self: _ClientMixin[_M], resource_id: str, options: Mapping[str, Union[int, str]] = {}, timeout: Optional[httpx.Timeout] = None) -> BaseModel:
        """Execute `destroy` command."""
        # Send request and save response
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class FindAllCommandMixin(Generic[_M]):
    """Client mixin with `find_all` command."""

    def find_all(self: _ClientMixin[_M], options: Mapping[str, Union[int, str]] = {}, timeout: Optional[httpx.Timeout] = None) -> Mapping[str, Any]:
        """Execute `find all` command."""
        # Send request and save response
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, ),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )


class FindCommandMixin(Generic[_M]):
    """Client mixin with `find` command."""

    def find(self: _ClientMixin[_M], resource_id: str, params: Mapping[str, str] = {}, timeout: Optional[httpx.Timeout] = None) -> _M:
        """Execute `find` command."""
        # Send request and save response
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id),
                query_pairs=params,
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class UpdateCommandMixin(Generic[_M]):
    """Client mixin with `update` command."""

    def update(self: _ClientMixin[_M], input_object: BaseModel, identifier: Optional[str] = None, timeout: Optional[httpx.Timeout] = None) -> _M:
        """Execute `update` command."""
        # Send request and save response
        api_response: Response = send_put_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, identifier) if identifier else (self.API_RESOURCE, ),
            ),
            content=to_json({
                self.ROOT_NAME: input_object.dict(exclude_none=True),
            }),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        # Process response data
        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
