from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import (
    CreateCommandMixin,
    DestroyCommandMixin,
    FindAllCommandMixin,
    FindCommandMixin,
    UpdateCommandMixin,
)
from ..models.webhook_endpoint import WebhookEndpointResponse


class WebhookEndpointClient(
    CreateCommandMixin[WebhookEndpointResponse],
    DestroyCommandMixin[WebhookEndpointResponse],
    FindAllCommandMixin[WebhookEndpointResponse],
    FindCommandMixin[WebhookEndpointResponse],
    UpdateCommandMixin[WebhookEndpointResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "webhook_endpoints"
    RESPONSE_MODEL: ClassVar[Type[WebhookEndpointResponse]] = WebhookEndpointResponse
    ROOT_NAME: ClassVar[str] = "webhook_endpoint"
