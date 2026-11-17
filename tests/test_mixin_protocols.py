from typing import Tuple, Type

from lago_python_client.client import Client
from lago_python_client.customers.applied_coupons_client import CustomerAppliedCouponsClient
from lago_python_client.mixins import _ChildClientMixin, _ClientMixin, _NestedClientMixin
from lago_python_client.models.applied_coupon import AppliedCouponResponse
from lago_python_client.models.subscription import SubscriptionResponse
from lago_python_client.subscriptions.alert_client import SubscriptionAlertClient
from lago_python_client.subscriptions.charges_client import SubscriptionChargesClient
from lago_python_client.subscriptions.clients import SubscriptionClient


def accept_client_mixin(client: _ClientMixin[SubscriptionResponse]) -> Type[SubscriptionResponse]:
    return client.RESPONSE_MODEL


def accept_child_client_mixin(client: _ChildClientMixin[AppliedCouponResponse]) -> str:
    return client.PARENT_API_RESOURCE


def accept_nested_client_mixin(client: _NestedClientMixin) -> Tuple[str, ...]:
    return client.api_resource("sub_1")


def test_client_mixin_protocols_and_classvars():
    client = Client(api_key="test-key")
    sub_client = SubscriptionClient(client.base_api_url, client.api_key)
    charges_client = SubscriptionChargesClient(client.base_api_url, client.api_key)
    applied_coupons_client = CustomerAppliedCouponsClient(client.base_api_url, client.api_key)
    alert_client = SubscriptionAlertClient(client.base_api_url, client.api_key)

    assert accept_client_mixin(sub_client) is SubscriptionResponse
    assert accept_child_client_mixin(applied_coupons_client) == "customers"
    assert accept_nested_client_mixin(alert_client) == ("subscriptions", "sub_1", "alerts")
    assert charges_client.PARENT_API_RESOURCE == "subscriptions"
    assert sub_client.API_RESOURCE == "subscriptions"
