from typing import ClassVar, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import DEFAULT_TIMEOUT, FindCommandMixin
from ..models.quote import QuoteVersionApprove, QuoteVersionResponse
from ..services.json import to_json
from ..services.request import (
    make_headers,
    make_url,
    send_post_request,
)
from ..services.response import Response, get_response_data, prepare_object_response


class QuoteVersionClient(
    FindCommandMixin[QuoteVersionResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "quote_versions"
    RESPONSE_MODEL: ClassVar[Type[QuoteVersionResponse]] = QuoteVersionResponse
    ROOT_NAME: ClassVar[str] = "quote_version"

    def approve(
        self,
        resource_id: str,
        input_object: Optional[QuoteVersionApprove] = None,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> QuoteVersionResponse:
        """Approve a draft version and generate the order form to sign."""
        payload = input_object.dict(exclude_none=True) if input_object else {}

        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "approve"),
            ),
            content=to_json(payload) if payload else None,
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def void(
        self,
        resource_id: str,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> QuoteVersionResponse:
        """Void a draft version, which makes it definitive."""
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "void"),
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def clone(
        self,
        resource_id: str,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> QuoteVersionResponse:
        """Copy a version into a new draft version of the same quote."""
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "clone"),
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
