import sys
from typing import Any, ClassVar, Type, Union

from pydantic import BaseModel

from .base_client import BaseClient
from ..mixins import DestroyCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.wallet_transaction import WalletTransactionResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_get_request, send_post_request
from ..services.response import get_response_data, prepare_create_response, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class WalletTransactionClient(
    DestroyCommandMixin[WalletTransactionResponse],
    FindCommandMixin[WalletTransactionResponse],
    UpdateCommandMixin[WalletTransactionResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'wallet_transactions'
    RESPONSE_MODEL: ClassVar[Type[WalletTransactionResponse]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = 'wallet_transactions'

    def create(self, input_object: BaseModel) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, ),
            ),
            data=to_json({
                'wallet_transaction': input_object.dict()
            }),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_create_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def find_all(self, wallet_id: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        api_response: Response = send_get_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('wallets', wallet_id, self.API_RESOURCE),
                query_pairs=options,
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_index_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response),
        )
