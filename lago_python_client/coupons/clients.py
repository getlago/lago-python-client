from typing import ClassVar, Type

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.coupon import CouponResponse
from ..models.applied_coupon import AppliedCouponResponse
from ..services.request import make_headers, make_url, send_delete_request
from ..services.response import get_response_data, prepare_object_response, Response


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


class AppliedCouponClient(CreateCommandMixin[AppliedCouponResponse], FindAllCommandMixin[AppliedCouponResponse], BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[AppliedCouponResponse]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def destroy(self, external_customer_id: str, applied_coupon_id: str) -> AppliedCouponResponse:
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
