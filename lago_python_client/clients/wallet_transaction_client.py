import requests
from typing import Any, ClassVar, Dict, Sequence, Type

from pydantic import BaseModel
from .base_client import BaseClient
from requests import Response
from lago_python_client.models.wallet_transaction import WalletTransactionResponse
from ..services.json import from_json, to_json
from ..services.request import make_url
from ..services.response import verify_response


class WalletTransactionClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'wallet_transactions'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = 'wallet_transactions'

    def create(self, input_object: BaseModel):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=(self.API_RESOURCE, ),
        )
        query_parameters = {
            'wallet_transaction': input_object.dict()
        }
        data = to_json(query_parameters)
        api_response = requests.post(query_url, data=data, headers=self.headers())
        data = verify_response(api_response)

        return self.prepare_response(from_json(data).get(self.ROOT_NAME))

    def find_all(self, wallet_id: str, options: dict = {}):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=('wallets', wallet_id, self.API_RESOURCE),
            query_pairs=options,
        )
        api_response = requests.get(query_url, headers=self.headers())
        data = from_json(verify_response(api_response))

        return self.prepare_index_response(data)

    @classmethod
    def prepare_response(cls, data: Sequence[Dict[Any, Any]]) -> Dict[str, Any]:
        return {
            cls.API_RESOURCE: [cls.prepare_object_response(response_model=cls.RESPONSE_MODEL, data=el) for el in data],
        }
