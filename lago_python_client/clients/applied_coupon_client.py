from .base_client import BaseClient
from lago_python_client.models.applied_coupon import AppliedCouponResponse
from typing import Dict


class AppliedCouponClient(BaseClient):
    def api_resource(self):
        return 'applied_coupons'

    def root_name(self):
        return 'applied_coupon'

    def prepare_response(self, data: Dict):
        return AppliedCouponResponse.parse_obj(data)
