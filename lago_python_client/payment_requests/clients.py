import sys
from typing import Any, ClassVar, Type, Union

from ..base_client import BaseClient
from ..mixins import FindAllCommandMixin
from ..models.payment_request import PaymentRequestResponse
from ..services.request import make_headers, make_url, send_get_request
from ..services.response import get_response_data, prepare_index_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


class PaymentRequestClient(
    FindAllCommandMixin[PaymentRequestResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'payment_requests'
    RESPONSE_MODEL: ClassVar[Type[PaymentRequestResponse]] = PaymentRequestResponse
    ROOT_NAME: ClassVar[str] = 'payment_request'
