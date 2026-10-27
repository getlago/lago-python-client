from typing import Any, ClassVar, Mapping, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import (
    NestedCreateCommandMixin,
    NestedDestroyCommandMixin,
    NestedFindAllCommandMixin,
    NestedFindCommandMixin,
    NestedUpdateCommandMixin,
)
from ..models.alert import Alert, AlertResponse
from ..services.request import QueryPairs


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

    # The API only looks up active subscriptions unless `subscription_status` is given.
    def create(
        self,
        subscription_id: str,
        input_object: Alert,
        subscription_status: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ) -> Optional[AlertResponse]:
        return super().create(
            subscription_id, input_object, options=_status_query(subscription_status), timeout=timeout
        )

    def update(
        self,
        subscription_id: str,
        code: str,
        input_object: Alert,
        subscription_status: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ) -> AlertResponse:
        return super().update(
            subscription_id, code, input_object, options=_status_query(subscription_status), timeout=timeout
        )

    def destroy(
        self,
        subscription_id: str,
        code: str,
        subscription_status: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ) -> AlertResponse:
        return super().destroy(subscription_id, code, options=_status_query(subscription_status), timeout=timeout)

    def find(
        self,
        subscription_id: str,
        code: str,
        subscription_status: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ) -> AlertResponse:
        return super().find(subscription_id, code, options=_status_query(subscription_status), timeout=timeout)

    def find_all(
        self,
        subscription_id: str,
        options: QueryPairs = None,
        subscription_status: Optional[str] = None,
        timeout: Optional[httpx.Timeout] = None,
    ) -> Mapping[str, Any]:
        query = {**dict(options or {}), **_status_query(subscription_status)}
        return super().find_all(subscription_id, options=query, timeout=timeout)


def _status_query(subscription_status: Optional[str]) -> dict:
    return {} if subscription_status is None else {"subscription_status": subscription_status}
