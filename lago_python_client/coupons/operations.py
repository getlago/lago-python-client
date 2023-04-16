import sys
from typing import ClassVar, Type

from ..base_operation import BaseOperation
from ..models.coupon import CouponResponse
from ..models.applied_coupon import AppliedCouponResponse
from ..services.request import make_headers, make_url, send_delete_request
from ..services.response import get_response_data, prepare_object_response, Response
from ..shared_operations import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin

if sys.version_info >= (3, 9):
    from collections.abc import Callable, Mapping
else:
    from typing import Callable, Mapping


class ApplyCoupon(CreateCommandMixin[AppliedCouponResponse], BaseOperation):
    """Apply a coupon to a customer."""

    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[AppliedCouponResponse]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'


class CreateCoupon(CreateCommandMixin[CouponResponse], BaseOperation):
    """Create a new coupon."""

    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'


class DeleteAppliedCoupon(BaseOperation):
    """Delete customer's appplied coupon."""

    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[AppliedCouponResponse]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def __call__(self, external_customer_id: str, applied_coupon_id: str) -> AppliedCouponResponse:
        api_response: Response = send_delete_request(
            url=make_url(
                origin=self.base_url,
                path_parts=('customers', external_customer_id, self.API_RESOURCE, applied_coupon_id),
            ),
            headers=make_headers(api_key=self.api_key),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )


class DestroyCoupon(DestroyCommandMixin[CouponResponse], BaseOperation):
    """Delete a coupon."""

    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'


class FindAllAppliedCoupons(FindAllCommandMixin[AppliedCouponResponse], BaseOperation):
    """Find Applied Coupons."""

    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[AppliedCouponResponse]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'


class FindAllCoupons(FindAllCommandMixin[CouponResponse], BaseOperation):
    """Find Coupons."""

    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'


class FindCoupon(FindCommandMixin[CouponResponse], BaseOperation):
    """Find coupon by code."""

    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'


class UpdateCoupon(UpdateCommandMixin[CouponResponse], BaseOperation):
    """Update an existing coupon."""

    API_RESOURCE: ClassVar[str] = 'coupons'
    RESPONSE_MODEL: ClassVar[Type[CouponResponse]] = CouponResponse
    ROOT_NAME: ClassVar[str] = 'coupon'


coupons_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': CreateCoupon,
    'destroy': DestroyCoupon,
    'find': FindCoupon,
    'find_all': FindAllCoupons,
    'update': UpdateCoupon,
}

applied_coupons_operations_config: Mapping[str, Callable[..., Callable]] = {
    'create': ApplyCoupon,
    'destroy': DeleteAppliedCoupon,
    'find_all': FindAllAppliedCoupons,
}
