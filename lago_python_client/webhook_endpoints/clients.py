import sys
from typing import Any, ClassVar, Type, Union

from pydantic import BaseModel

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.webhook_endpoint import WebhookEndpointResponse
from ..services.json import to_json
from ..services.request import make_headers, make_url, send_get_request, send_post_request
from ..services.response import get_response_data, prepare_object_list_response, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class WebhookEndpointClient(
    CreateCommandMixin[WebhookEndpointResponse],
    DestroyCommandMixin[WebhookEndpointResponse],
    FindAllCommandMixin[WebhookEndpointResponse],
    FindCommandMixin[WebhookEndpointResponse],
    UpdateCommandMixin[WebhookEndpointResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'webhook_endpoints'
    RESPONSE_MODEL: ClassVar[Type[WebhookEndpointResponse]] = WebhookEndpointResponse
    ROOT_NAME: ClassVar[str] = 'webhook_endpoint'
