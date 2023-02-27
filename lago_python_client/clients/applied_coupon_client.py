import requests

from .base_client import BaseClient
from lago_python_client.models.applied_coupon import AppliedCouponResponse
from typing import Dict
from urllib.parse import urljoin
from requests import Response
from ..services.json import from_json

class AppliedCouponClient(BaseClient):
    def api_resource(self):
        return 'applied_coupons'

    def root_name(self):
        return 'applied_coupon'

    def prepare_response(self, data: Dict):
        return AppliedCouponResponse.parse_obj(data)

    def destroy(self, external_customer_id: str, applied_coupon_id: str):
        api_resource = 'customers/' + external_customer_id + '/applied_coupons/' + applied_coupon_id
        query_url = urljoin(self.base_url, api_resource)

        api_response = requests.delete(query_url, headers=self.headers())
        data = from_json(self.handle_response(api_response)).get(self.root_name())

        return self.prepare_response(data)
