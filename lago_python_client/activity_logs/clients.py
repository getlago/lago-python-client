from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    FindAllCommandMixin,
    FindCommandMixin,
)
from ..models.activity_log import ActivityLogResponse


class ActivityLogClient(
    FindAllCommandMixin[ActivityLogResponse],
    FindCommandMixin[ActivityLogResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "activity_logs"
    RESPONSE_MODEL: ClassVar[Type[ActivityLogResponse]] = ActivityLogResponse
    ROOT_NAME: ClassVar[str] = "activity_log"
