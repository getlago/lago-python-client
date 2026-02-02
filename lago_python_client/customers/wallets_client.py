from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.wallet import WalletResponse
from ..client import CustomerClient


class CustomerWalletsClient(
    CreateCommandMixin[WalletResponse],
    DestroyCommandMixin[WalletResponse],
    FindAllCommandMixin[WalletResponse],
    FindCommandMixin[WalletResponse],
    UpdateCommandMixin[WalletResponse],
    BaseClient
):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "wallets"
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = "wallet"
