import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Subscription


def create_subscription():
    return Subscription(
        external_customer_id="5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba",
        plan_code="eartha lynch",
        external_id="code",
        billing_time="anniversary",
        subscription_at="2022-04-29T08:59:51Z",
        ending_at="2022-08-29T08:59:51Z",
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/subscription.json")

    with open(my_data_path, "rb") as subscription_response:
        return subscription_response.read()


def mock_lifetime_usage_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/lifetime_usage.json")

    with open(my_data_path, "rb") as subscription_response:
        return subscription_response.read()


def mock_update_lifetime_usage_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/update_lifetime_usage.json")

    with open(my_data_path, "rb") as subscription_response:
        return subscription_response.read()


def mock_response_for_pending():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/pending_subscription.json")

    with open(my_data_path, "rb") as subscription_response:
        return subscription_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/subscription_index.json")

    with open(data_path, "rb") as subscription_response:
        return subscription_response.read()


def test_valid_create_subscriptions_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/subscriptions",
        content=mock_response(),
    )
    response = client.subscriptions.create(create_subscription())

    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.status == "active"
    assert response.plan_code == "eartha lynch"
    assert response.billing_time == "anniversary"
    assert response.subscription_at == "2022-04-29T08:59:51Z"
    assert response.ending_at == "2022-08-29T08:59:51Z"


def test_invalid_create_subscriptions_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/subscriptions",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.create(create_subscription())


def test_valid_update_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    identifier = "sub_id"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/subscriptions/" + identifier,
        content=mock_response(),
    )
    response = client.subscriptions.update(Subscription(name="name"), identifier)

    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.status == "active"
    assert response.plan_code == "eartha lynch"
    assert response.billing_time == "anniversary"
    assert response.subscription_at == "2022-04-29T08:59:51Z"


def test_invalid_update_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    identifier = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/subscriptions/" + identifier,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.update(Subscription(name="name"), identifier)


def test_valid_destroy_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    identifier = "sub_id"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/" + identifier,
        content=mock_response(),
    )
    response = client.subscriptions.destroy(identifier)

    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.status == "active"
    assert response.plan_code == "eartha lynch"


def test_valid_destroy_subscription_with_on_termination_actions_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    identifier = "sub_id"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/"
        + identifier
        + "?on_termination_credit_note=skip&on_termination_invoice=skip",
        content=mock_response(),
    )
    response = client.subscriptions.destroy(
        identifier, {"on_termination_credit_note": "skip", "on_termination_invoice": "skip"}
    )

    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.status == "active"
    assert response.plan_code == "eartha lynch"
    assert response.on_termination_credit_note == "skip"
    assert response.on_termination_invoice == "skip"


def test_valid_destroy_pending_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    identifier = "sub_id"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/" + identifier + "?status=pending",
        content=mock_response_for_pending(),
    )
    response = client.subscriptions.destroy(identifier, {"status": "pending"})
    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"
    assert response.status == "pending"
    assert response.plan_code == "eartha lynch"


def test_invalid_destroy_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    identifier = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/subscriptions/" + identifier,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.destroy(identifier)


def test_valid_find_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id,
        content=mock_response(),
    )
    response = client.subscriptions.find(external_id)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.external_customer_id == "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"


def test_invalid_find_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    external_id = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.find(external_id)


def test_valid_find_all_subscription_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions?external_customer_id=123",
        content=mock_collection_response(),
    )
    response = client.subscriptions.find_all({"external_customer_id": "123"})

    assert response["subscriptions"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_subscription_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.subscriptions.find_all()


def test_valid_lifetime_usage_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id + "/lifetime_usage",
        content=mock_lifetime_usage_response(),
    )
    response = client.subscriptions.lifetime_usage(external_id)

    assert response.lago_id == "ef555447-b017-4345-9846-6b814cfb4148"
    assert response.current_usage_amount_cents == 3000
    assert response.usage_thresholds[0].amount_cents == 2000
    assert response.usage_thresholds[0].completion_ratio == 1
    assert response.usage_thresholds[1].amount_cents == 4000
    assert response.usage_thresholds[1].completion_ratio == 0.5


def test_invalid_lifetime_usage_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "notfound"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id + "/lifetime_usage",
        status_code=404,
        content=b"",
    )
    with pytest.raises(LagoApiError):
        client.subscriptions.lifetime_usage(external_id)


def test_update_lifetime_usage_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "5eb02857-a71e-4ea2-bcf9-57d3a41bc6ba"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id + "/lifetime_usage",
        content=mock_update_lifetime_usage_response(),
    )
    response = client.subscriptions.update_lifetime_usage(external_id, 2000)

    assert response.lago_id == "ef555447-b017-4345-9846-6b814cfb4148"
    assert response.external_historical_usage_amount_cents == 2000


def mock_fixed_charges_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/fixed_charges.json")

    with open(my_data_path, "rb") as fixed_charges_response:
        return fixed_charges_response.read()


def test_valid_find_all_fixed_charges_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "sub_external_123"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id + "/fixed_charges",
        content=mock_fixed_charges_response(),
    )
    response = client.subscriptions.find_all_fixed_charges(external_id)

    assert len(response["fixed_charges"]) == 2
    assert response["fixed_charges"][0].lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["fixed_charges"][0].invoice_display_name == "Setup Fee"
    assert response["fixed_charges"][0].charge_model == "standard"
    assert response["fixed_charges"][0].pay_in_advance is True
    assert response["fixed_charges"][0].prorated is False
    assert response["fixed_charges"][0].properties.amount == "500"
    assert response["fixed_charges"][0].units == 1.0
    assert response["fixed_charges"][1].lago_id == "3c903c90-3c90-3c90-3c90-3c903c903c90"
    assert response["fixed_charges"][1].charge_model == "graduated"
    assert response["fixed_charges"][1].properties.graduated_ranges[0].from_value == 0
    assert response["fixed_charges"][1].properties.graduated_ranges[0].per_unit_amount == "100"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_fixed_charges_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    external_id = "invalid_sub"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/subscriptions/" + external_id + "/fixed_charges",
        status_code=404,
        content=b"",
    )
    with pytest.raises(LagoApiError):
        client.subscriptions.find_all_fixed_charges(external_id)


def test_fixed_charge_response_model_parsing():
    from lago_python_client.models.fixed_charge import FixedChargeResponse

    # Test standard charge model
    standard_data = {
        "lago_id": "1a901a90-1a90-1a90-1a90-1a901a901a90",
        "lago_add_on_id": "2b902b90-2b90-2b90-2b90-2b902b902b90",
        "invoice_display_name": "Setup Fee",
        "add_on_code": "setup_fee",
        "created_at": "2024-01-15T10:00:00Z",
        "code": "setup",
        "charge_model": "standard",
        "pay_in_advance": True,
        "prorated": False,
        "properties": {"amount": "500"},
        "units": 1.0,
        "lago_parent_id": None,
        "taxes": [],
    }

    response = FixedChargeResponse(**standard_data)
    assert response.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.charge_model == "standard"
    assert response.properties.amount == "500"
    assert response.pay_in_advance is True

    # Test graduated charge model
    graduated_data = {
        "lago_id": "3c903c90-3c90-3c90-3c90-3c903c903c90",
        "lago_add_on_id": "4d904d90-4d90-4d90-4d90-4d904d904d90",
        "invoice_display_name": "Support Tiers",
        "add_on_code": "support",
        "created_at": "2024-01-15T10:00:00Z",
        "code": None,
        "charge_model": "graduated",
        "pay_in_advance": False,
        "prorated": True,
        "properties": {
            "graduated_ranges": [
                {"from_value": 0, "to_value": 10, "flat_amount": "0", "per_unit_amount": "100"},
                {"from_value": 11, "to_value": None, "flat_amount": "50", "per_unit_amount": "80"},
            ]
        },
        "units": 5.0,
        "lago_parent_id": None,
        "taxes": [],
    }

    response = FixedChargeResponse(**graduated_data)
    assert response.charge_model == "graduated"
    assert len(response.properties.graduated_ranges) == 2
    assert response.properties.graduated_ranges[0].from_value == 0
    assert response.properties.graduated_ranges[0].per_unit_amount == "100"
    assert response.properties.graduated_ranges[1].to_value is None
