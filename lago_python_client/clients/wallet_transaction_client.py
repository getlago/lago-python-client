import requests
import sys
from typing import Any, ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.wallet_transaction import WalletTransactionResponse
from ..services.json import from_json, to_json
from ..services.request import make_url
from ..services.response import prepare_create_response, prepare_index_response, verify_response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class WalletTransactionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'wallet_transactions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = 'wallet_transactions'

    def create(self, input_object: BaseModel) -> Mapping[str, Any]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
        )
        query_parameters = {
            'wallet_transaction': input_object.dict()
        }
        data = to_json(query_parameters)
        api_response: Response = requests.post(query_url, data=data, headers=self.headers())

        return prepare_create_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )

    def find_all(self, wallet_id: str, options: dict = {}) -> Mapping[str, Any]:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=('wallets', wallet_id, self.API_RESOURCE),
            query_pairs=options,
        )
        api_response: Response = requests.get(query_url, headers=self.headers())

        return prepare_index_response(
            api_resourse=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)),
        )
