from typing import ClassVar, Type

from ..base_client import BaseClient
from ..models.alert import AlertResponse

from ..mixins import (
    NestedCreateCommandMixin,
    NestedUpdateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindCommandMixin,
    NestedFindAllCommandMixin,
)


class SubscriptionAlertClient(
    NestedCreateCommandMixin[AlertResponse],
    NestedUpdateCommandMixin[AlertResponse],
    NestedDestroyCommandMixin[AlertResponse],
    NestedFindCommandMixin[AlertResponse],
    NestedFindAllCommandMixin[AlertResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "alerts"
    RESPONSE_MODEL: ClassVar[Type[AlertResponse]] = AlertResponse
    ROOT_NAME: ClassVar[str] = "alert"

    def api_resource(self, subscription_id: str) -> tuple[str]:
        return ("subscriptions", subscription_id, "alerts")
