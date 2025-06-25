from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    FindAllCommandMixin,
    FindCommandMixin,
)
from ..models.api_log import ApiLogResponse


class ApiLogClient(
    FindAllCommandMixin[ApiLogResponse],
    FindCommandMixin[ApiLogResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "api_logs"
    RESPONSE_MODEL: ClassVar[Type[ApiLogResponse]] = ApiLogResponse
    ROOT_NAME: ClassVar[str] = "api_log"
