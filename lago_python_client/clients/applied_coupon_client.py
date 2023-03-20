import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..models.applied_coupon import AppliedCouponResponse
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import prepare_object_response, verify_response


class AppliedCouponClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def destroy(self, external_customer_id: str, applied_coupon_id: str) -> BaseModel:
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=('customers', external_customer_id, self.API_RESOURCE, applied_coupon_id),
        )
        api_response: Response = requests.delete(query_url, headers=self.headers())

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=from_json(verify_response(api_response)).get(self.ROOT_NAME),
        )
