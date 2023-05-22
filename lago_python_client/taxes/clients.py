from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.tax import TaxResponse


class TaxClient(
    CreateCommandMixin[TaxResponse],
    DestroyCommandMixin[TaxResponse],
    FindAllCommandMixin[TaxResponse],
    FindCommandMixin[TaxResponse],
    UpdateCommandMixin[TaxResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'taxes'
    RESPONSE_MODEL: ClassVar[Type[TaxResponse]] = TaxResponse
    ROOT_NAME: ClassVar[str] = 'tax'
