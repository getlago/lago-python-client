import sys
from typing import Any, ClassVar, Type, Union

from pydantic import BaseModel

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.wallet import WalletResponse
from ..models.wallet_transaction import WalletTransactionResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_get_request, send_post_request
from ..services.response import get_response_data, prepare_object_list_response, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class WalletClient(
    CreateCommandMixin[WalletResponse],
    DestroyCommandMixin[WalletResponse],
    FindAllCommandMixin[WalletResponse],
    FindCommandMixin[WalletResponse],
    UpdateCommandMixin[WalletResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize client instance with internal ``WalletTransactionClient`` client instance."""
        super().__init__(base_url=base_url, api_key=api_key)
        self._wallet_transactions: WalletTransactionClient = WalletTransactionClient(base_url=base_url, api_key=api_key)

    def create_transaction(self, input_object: BaseModel) -> Mapping[str, Any]:
        """Create a wallet transaction."""
        return self._wallet_transactions.create(input_object=input_object)

    def find_all_transactions(self, wallet_id: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        """Find all wallet transactions."""
        return self._wallet_transactions.find_all(wallet_id=wallet_id, options=options)


class WalletTransactionClient(BaseClient):
    """Wallet transactions collection client.

    Pending deprecation warning: class methods are not for public use. If you going to add new methods then register aliases in `WalletClient`.
    """

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

        return prepare_object_list_response(
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
