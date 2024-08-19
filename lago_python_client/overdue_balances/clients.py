import sys
from typing import Any, ClassVar, Type, Union

from ..base_client import BaseClient
from ..mixins import FindAllCommandMixin
from ..models.overdue_balance import OverdueBalanceResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class OverdueBalanceClient(
    FindAllCommandMixin[OverdueBalanceResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'overdue_balances'
    RESPONSE_MODEL: ClassVar[Type[OverdueBalanceResponse]] = OverdueBalanceResponse
    ROOT_NAME: ClassVar[str] = 'overdue_balance'

    def find_all(self, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('analytics', 'overdue_balance'),
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
