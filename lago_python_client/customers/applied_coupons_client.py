from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import FindAllChildrenCommandMixin
from ..models.applied_coupon import AppliedCouponResponse
from ..client import CustomerClient


class CustomerAppliedCouponsClient(FindAllChildrenCommandMixin, BaseClient):
    PARENT_API_RESOURCE: ClassVar[str] = CustomerClient.API_RESOURCE
    API_RESOURCE: ClassVar[str] = "applied_coupons"
    RESPONSE_MODEL: ClassVar[Type[AppliedCouponResponse]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = "applied_coupon"
