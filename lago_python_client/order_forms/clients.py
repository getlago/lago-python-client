from typing import ClassVar, Optional, Type

import httpx

from ..base_client import BaseClient
from ..mixins import (
    DEFAULT_TIMEOUT,
    FindAllCommandMixin,
    FindCommandMixin,
)
from ..models.order_form import OrderFormMarkAsSigned, OrderFormResponse
from ..services.json import to_json
from ..services.request import (
    make_headers,
    make_url,
    send_post_request,
)
from ..services.response import Response, get_response_data, prepare_object_response


class OrderFormClient(
    FindCommandMixin[OrderFormResponse],
    FindAllCommandMixin[OrderFormResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = "order_forms"
    RESPONSE_MODEL: ClassVar[Type[OrderFormResponse]] = OrderFormResponse
    ROOT_NAME: ClassVar[str] = "order_form"

    def mark_as_signed(
        self,
        resource_id: str,
        input_object: Optional[OrderFormMarkAsSigned] = None,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> OrderFormResponse:
        """Record the customer's signature and create the order carrying the deal out."""
        payload = input_object.dict(exclude_none=True) if input_object else {}

        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "mark_as_signed"),
            ),
            content=to_json({self.ROOT_NAME: payload}) if payload else None,
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )

    def void(
        self,
        resource_id: str,
        timeout: Optional[httpx.Timeout] = DEFAULT_TIMEOUT,
    ) -> OrderFormResponse:
        """Void a generated order form, cascading to the quote version it came from."""
        api_response: Response = send_post_request(
            url=make_url(
                origin=self.base_url,
                path_parts=(self.API_RESOURCE, resource_id, "void"),
            ),
            headers=make_headers(api_key=self.api_key),
            timeout=timeout,
            rate_limit_retry_config=self.rate_limit_retry_config,
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
