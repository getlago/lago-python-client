import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.applied_coupon import AppliedCouponResponse
from requests import Response
from ..services.json import from_json
from ..services.request import make_url
from ..services.response import verify_response


class AppliedCouponClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def destroy(self, external_customer_id: str, applied_coupon_id: str):
        query_url: str = make_url(
            origin=self.base_url,
            path_parts=('customers', external_customer_id, self.API_RESOURCE, applied_coupon_id),
        )
        api_response = requests.delete(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_object_response(response_model=self.RESPONSE_MODEL, data=data)
