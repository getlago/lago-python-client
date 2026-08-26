from typing import Any, ClassVar, Mapping, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import (
    DEFAULT_TIMEOUT,
    FindAllCommandMixin,
    FindCommandMixin,
)
from ..models.quote import QuoteResponse, QuoteVersionResponse
from ..services.request import (
    QueryPairs,
    make_headers,
    make_url,
    send_get_request,
)
from ..services.response import Response, get_response_data, prepare_index_response


class QuoteClient(
    FindCommandMixin[QuoteResponse],
    FindAllCommandMixin[QuoteResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "quotes"
    RESPONSE_MODEL: ClassVar[Type[QuoteResponse]] = QuoteResponse
    ROOT_NAME: ClassVar[str] = "quote"

    VERSIONS_API_RESOURCE: ClassVar[str] = "quote_versions"

    def versions(
        self,
        resource_id: str,
        options: QueryPairs = None,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> Mapping[str, Any]:
        """List the versions of a quote, from the most recent to the oldest."""
        if options is None:
            options = {}
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "versions"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_index_response(
            api_resource=self.VERSIONS_API_RESOURCE,
            response_model=QuoteVersionResponse,
            data=get_response_data(response=api_response),
        )
