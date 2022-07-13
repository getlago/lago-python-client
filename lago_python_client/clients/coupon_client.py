from .base_client import BaseClient
from lago_python_client.models.coupon import CouponResponse
from typing import Dict


class CouponClient(BaseClient):
    def api_resource(self):
        return 'coupons'

    def root_name(self):
        return 'coupon'

    def prepare_response(self, data: Dict):
        return CouponResponse.parse_obj(data)
