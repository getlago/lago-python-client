from collections.abc import Mapping
from typing import Any, ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllCommandMixin
from ..models.usage import UsageResponse
from ..services.request import QueryPairs, make_headers, make_url, send_get_request
from ..services.response import Response, get_response_data, prepare_index_response


class UsageClient(
    FindAllCommandMixin[UsageResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "usages"
    RESPONSE_MODEL: ClassVar[Type[UsageResponse]] = UsageResponse
    ROOT_NAME: ClassVar[str] = "usage"

    def find_all(self, options: QueryPairs = None) -> Mapping[str, Any]:
        if options is None:
            options = {}
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=("analytics", "usage"),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        # Process response data
        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )
