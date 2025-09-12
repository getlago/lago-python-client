import sys
from typing import Any, ClassVar, Optional, Type

import httpx

from ..base_client import BaseClient
from ..models.invoice import InvoiceResponse
from ..client import CustomerClient
from ..services.request import (
    QueryPairs,
    make_headers,
    make_url,
    send_get_request,
)
from ..services.response import (
    get_response_data,
    prepare_index_response,
    Response,
)

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class CustomerInvoicesClient(BaseClient):
    API_RESOURCE: ClassVar[str] = "invoices"
    RESPONSE_MODEL: ClassVar[Type[InvoiceResponse]] = InvoiceResponse
    ROOT_NAME: ClassVar[str] = "invoice"

    def find_all(
        self,
        resource_id: str,
        options: QueryPairs = {},
        timeout: Optional[httpx.Timeout] = None,
    ) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(
                    CustomerClient.API_RESOURCE,
                    resource_id,
                    self.API_RESOURCE,
                ),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
        )

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )
