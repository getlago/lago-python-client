from typing import ClassVar, Type

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.coupon import CouponResponse


class CouponClient(
    CreateCommandMixin[CouponResponse],
    DestroyCommandMixin[CouponResponse],
    FindAllCommandMixin[CouponResponse],
    FindCommandMixin[CouponResponse],
    UpdateCommandMixin[CouponResponse],
    BaseClient,
):
    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'
