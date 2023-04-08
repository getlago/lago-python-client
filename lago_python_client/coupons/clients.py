import sys
from typing import Any, ClassVar, Optional, Type, Union

from pydantic import BaseModel

from ..base_client import BaseClient
from ..mixins import CreateCommandMixin, DestroyCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.coupon import CouponResponse
from ..models.applied_coupon import AppliedCouponResponse
from ..services.request import make_headers, make_url, send_delete_request
from ..services.response import get_response_data, prepare_object_response, Response

if sys.version_info >= (3, 9):
    from collections.abc import Mapping
else:
    from typing import Mapping


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

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize client instance with internal ``AppliedCouponClient`` client instance."""
        super().__init__(base_url=base_url, api_key=api_key)
        self._applied_coupons: AppliedCouponClient = AppliedCouponClient(base_url=base_url, api_key=api_key)

    def apply(self, input_object: BaseModel) -> Optional[AppliedCouponResponse]:
        """Apply a coupon."""
        return self._applied_coupons.create(input_object=input_object)

    def find_all_applied(self, options: Mapping[str, Union[int, str]] = {}) -> Mapping[str, Any]:
        """Find all applied coupons."""
        return self._applied_coupons.find_all(options=options)

    def delete_applied(self, external_customer_id: str, applied_coupon_id: str) -> AppliedCouponResponse:
        """Delete applied coupons."""
        return self._applied_coupons.destroy(external_customer_id=external_customer_id, applied_coupon_id=applied_coupon_id)


class AppliedCouponClient(CreateCommandMixin[AppliedCouponResponse], FindAllCommandMixin[AppliedCouponResponse], BaseClient):
    """Applied coupons collection client.

    Pending deprecation warning: class methods are not for public use. If you going to add new methods then register aliases in `CouponClient`.
    """

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
