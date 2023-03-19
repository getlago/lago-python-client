import requests
from typing import ClassVar, Type

from pydantic import BaseModel
from requests import Response

from .base_client import BaseClient
from ..mixins import CreateCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin
from ..models.applied_coupon import AppliedCouponResponse
from ..services.request import make_url
from ..services.response import get_response_data, prepare_object_response


class AppliedCouponClient(CreateCommandMixin, FindAllCommandMixin, FindCommandMixin, UpdateCommandMixin, BaseClient):
    API_RESOURCE: ClassVar[str] = 'applied_coupons'
    RESPONSE_MODEL: ClassVar[Type[BaseModel]] = AppliedCouponResponse
    ROOT_NAME: ClassVar[str] = 'applied_coupon'

    def destroy(self, external_customer_id: str, applied_coupon_id: str) -> BaseModel:
        api_response: Response = requests.delete(
            url=make_url(
                origin=self.base_url,
                path_parts=('customers', external_customer_id, self.API_RESOURCE, applied_coupon_id),
            ),
            headers=self.headers(),
        )

        return prepare_object_response(
            response_model=self.RESPONSE_MODEL,
            data=get_response_data(response=api_response, key=self.ROOT_NAME),
        )
