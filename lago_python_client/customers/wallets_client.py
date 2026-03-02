from typing import ClassVar, Type

from ..base_client import BaseClient
from ..client import CustomerClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.wallet import WalletResponse


class CustomerWalletsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "wallets"
    RESPONSE_MODEL: ClassVar[Type[WalletResponse]] = WalletResponse
    ROOT_NAME: ClassVar[str] = "wallet"
