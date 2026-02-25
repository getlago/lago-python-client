from collections.abc import Mapping
from typing import Any, ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllCommandMixin
from ..models.gross_revenue import GrossRevenueResponse
from ..services.request import QueryPairs, make_headers, make_url, send_get_request
from ..services.response import Response, get_response_data, prepare_index_response


class GrossRevenueClient(
    FindAllCommandMixin[GrossRevenueResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "gross_revenues"
    RESPONSE_MODEL: ClassVar[Type[GrossRevenueResponse]] = GrossRevenueResponse
    ROOT_NAME: ClassVar[str] = "gross_revenue"

    def find_all(self, options: QueryPairs = None) -> Mapping[str, Any]:
        if options is None:
            options = {}
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=("analytics", "gross_revenue"),
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
