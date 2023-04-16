import sys
from typing import Any, ClassVar, Type, Union

from pydantic import BaseModel

from ..base_operation import BaseOperation
from ..models.wallet import WalletResponse
from ..models.wallet_transaction import WalletTransactionResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_get_request, send_post_request
from ..services.response import get_response_data, prepare_object_list_response, prepare_index_response, Response
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class CreateWallet(CreateCommandMixin[WalletResponse], BaseOperation):
    """Create a new wallet."""

    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'


class DestroyWallet(DestroyCommandMixin[WalletResponse], BaseOperation):
    """Delete a wallet."""

    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'


class FindAllWallets(FindAllCommandMixin[WalletResponse], BaseOperation):
    """Find wallets."""

    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'


class FindWallet(FindCommandMixin[WalletResponse], BaseOperation):
    """Find wallet."""

    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'


class UpdateWallet(UpdateCommandMixin[WalletResponse], BaseOperation):
    """Update an existing wallet."""

    API_RESOURCE: ClassVar[str] = 'wallets'
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = 'wallet'


class CreateWalletTransaction(BaseOperation):
    """Create a new wallet transaction."""

    API_RESOURCE: ClassVar[str] = 'wallet_transactions'
    RESPONSE_MODEL: ClassVar[Type[WalletTransactionResponse]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = 'wallet_transactions'

    def __call__(self, input_object: BaseModel) -> Mapping[str, Any]:
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, ),
            ),
            content=to_json({
                'wallet_transaction': input_object.dict()
            }),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_list_response(
            api_resource=self.API_RESOURCE,
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class FindAllWalletTransactions(BaseOperation):
    """Find wallet transactions."""

    API_RESOURCE: ClassVar[str] = 'wallet_transactions'
    RESPONSE_MODEL: ClassVar[Type[WalletTransactionResponse]] = WalletTransactionResponse
    ROOT_NAME: ClassVar[str] = 'wallet_transactions'

    def __call__(self, wallet_id: str, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
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


wallets_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateWallet,
    'destroy': DestroyWallet,
    'find': FindWallet,
    'find_all': FindAllWallets,
    'update': UpdateWallet,
}

wallet_transactions_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateWalletTransaction,
    'find_all': FindAllWalletTransactions,
}
