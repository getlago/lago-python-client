from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindCommandMixin
from ..models.fee import FeeResponse


class FeeClient(FindCommandMixin[FeeResponse], BaseClient):
    API_RESOURCE: ClassVar[str] = 'fees'
    RESPONSE_MODEL: ClassVar[Type[FeeResponse]] = FeeResponse
    ROOT_NAME: ClassVar[str] = 'fee'
