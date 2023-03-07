from typing import ClassVar, Dict

from .base_client import BaseClient
from lago_python_client.models.coupon import CouponResponse


class CouponClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'coupons'
    ROOT_NAME: ClassVar[str] = 'coupon'

    def prepare_response(self, data: Dict):
        return CouponResponse.parse_obj(data)
