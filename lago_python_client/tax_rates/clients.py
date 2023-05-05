from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.tax_rate import TaxRateResponse


class TaxRateClient(
    CreateCommandMixin[TaxRateResponse],
    DestroyCommandMixin[TaxRateResponse],
    FindAllCommandMixin[TaxRateResponse],
    FindCommandMixin[TaxRateResponse],
    UpdateCommandMixin[TaxRateResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'tax_rates'
    RESPONSE_MODEL: ClassVar[Type[TaxRateResponse]] = TaxRateResponse
    ROOT_NAME: ClassVar[str] = 'tax_rate'
