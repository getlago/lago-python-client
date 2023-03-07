from typing import Any, ClassVar, Dict, Type

from pydantic import BaseModel
from .base_client import BaseClient
from lago_python_client.models.coupon import CouponResponse


class CouponClient(BaseClient):
    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'

    @classmethod
    def prepare_object_response(cls, data: Dict[Any, Any]) -> BaseModel:
        return cls.RESPONSE_MODEL.parse_obj(data)
