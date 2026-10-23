from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.usage_attribution_type import UsageAttributionTypeResponse


class UsageAttributionTypeClient(
    CreateCommandMixin[UsageAttributionTypeResponse],
    DestroyCommandMixin[UsageAttributionTypeResponse],
    FindAllCommandMixin[UsageAttributionTypeResponse],
    FindCommandMixin[UsageAttributionTypeResponse],
    UpdateCommandMixin[UsageAttributionTypeResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "usage_attribution_types"
    RESPONSE_MODEL: ClassVar[Type[UsageAttributionTypeResponse]] = UsageAttributionTypeResponse
    ROOT_NAME: ClassVar[str] = "usage_attribution_type"
