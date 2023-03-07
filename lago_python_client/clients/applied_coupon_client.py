import requests
from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.applied_coupon import AppliedCouponResponse
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json
from ..services.response import verify_response


class AppliedCouponClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def destroy(self, external_customer_id: str, applied_coupon_id: str):
        uri: str = '/'.join(('customers', external_customer_id, self.API_RESOURCE, applied_coupon_id))
        query_url: str = urljoin(self.base_url, uri)

        api_response = requests.delete(query_url, headers=self.headers())
        data = from_json(verify_response(api_response)).get(self.ROOT_NAME)

        return self.prepare_object_response(data)
