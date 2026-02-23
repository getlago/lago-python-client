import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import (
    Plan,
    Charge,
    Charges,
    ChargeFilters,
    ChargeFilter,
    MinimumCommitment,
    UsageThreshold,
    UsageThresholds,
    FixedCharge,
    FixedCharges,
    FixedChargeProperties,
)


def plan_object():
    charge = Charge(
        id=None,
        invoice_display_name=None,
        regroup_paid_fees=None,
        properties=None,
        tax_codes=None,
        billable_metric_id="id",
        charge_model="standard",
        pay_in_advance=True,
        invoiceable=False,
        prorated=False,
        min_amount_cents=0,
        filters=ChargeFilters(
            __root__=[
                ChargeFilter(
                    properties={"amount": "0.22"},
                    invoice_display_name="Europe",
                    values={"country": ["france", "italy", "spain"]},
                )
            ]
        ),
    )
    charges = Charges(__root__=[charge])

    usage_threshold = UsageThreshold(threshold_display_name="Threshold 1", amount_cents=20, recurring=False, id=None)

    usage_thresholds = UsageThresholds(__root__=[usage_threshold])

    minimum_commitment = MinimumCommitment(amount_cents=0, invoice_display_name="Commitment (C1)", tax_codes=None)

    return Plan(
        name="name",
        invoice_display_name="invoice_display_name",
        code="code_first",
        amount_cents=1000,
        amount_currency="EUR",
        description="desc",
        interval="weekly",
        pay_in_advance=True,
        charges=charges,
        minimum_commitment=minimum_commitment,
        usage_thresholds=usage_thresholds,
        trial_period=None,
        bill_charges_monthly=None,
        tax_codes=None,
        cascade_updates=None,
    )


def graduated_plan_object():
    charge = Charge(
        id=None,
        invoice_display_name=None,
        regroup_paid_fees=None,
        tax_codes=None,
        pay_in_advance=None,
        invoiceable=None,
        min_amount_cents=None,
        filters=None,
        billable_metric_id="id",
        charge_model="graduated",
        prorated=False,
        properties={
            "graduated_ranges": [
                {
                    "to_value": 1,
                    "from_value": 0,
                    "flat_amount": "0",
                    "per_unit_amount": "0",
                },
                {
                    "to_value": None,
                    "from_value": 2,
                    "flat_amount": "0",
                    "per_unit_amount": "3200",
                },
            ]
        },
    )
    charges = Charges(__root__=[charge])

    return Plan(
        invoice_display_name=None,
        tax_codes=None,
        bill_charges_monthly=None,
        trial_period=None,
        minimum_commitment=None,
        usage_thresholds=None,
        name="name",
        code="code_first",
        amount_cents=1000,
        amount_currency="EUR",
        description="desc",
        interval="weekly",
        pay_in_advance=True,
        charges=charges,
    )


def plan_with_fixed_charges_object():
    fixed_charge = FixedCharge(
        id=None,
        add_on_id="add_on_123",
        charge_model="standard",
        invoice_display_name="Setup Fee",
        units=1.0,
        pay_in_advance=True,
        prorated=False,
        properties=FixedChargeProperties(amount="500"),
        tax_codes=None,
        apply_units_immediately=None,
    )
    fixed_charges = FixedCharges(__root__=[fixed_charge])

    return Plan(
        invoice_display_name=None,
        tax_codes=None,
        bill_charges_monthly=None,
        bill_fixed_charges_monthly=True,
        trial_period=None,
        minimum_commitment=None,
        usage_thresholds=None,
        name="plan_with_fixed_charges",
        code="plan_fixed",
        amount_cents=10000,
        amount_currency="USD",
        description="Plan with fixed charges",
        interval="monthly",
        pay_in_advance=False,
        charges=None,
        fixed_charges=fixed_charges,
        cascade_updates=None,
    )


def mock_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan.json")

    with open(data_path, "rb") as plan_response:
        return plan_response.read()


def mock_graduated_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/graduated_plan.json")

    with open(data_path, "rb") as plan_response:
        return plan_response.read()


def mock_collection_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_index.json")

    with open(data_path, "rb") as plan_response:
        return plan_response.read()


def test_valid_create_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans",
        content=mock_response(),
    )
    response = client.plans.create(plan_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.code == "plan_code"
    assert response.invoice_display_name == "test plan 1"
    assert response.charges.__root__[0].invoice_display_name == "Setup"
    assert response.minimum_commitment.invoice_display_name == "Minimum commitment (C1)"
    assert response.usage_thresholds.__root__[0].threshold_display_name == "Threshold 1"
    assert response.metadata == {"key1": "value1", "key2": None}


def test_valid_create_graduated_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans",
        content=mock_graduated_response(),
    )
    response = client.plans.create(graduated_plan_object())

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.code == "plan_code"
    assert response.invoice_display_name == "test plan 1"


def test_invalid_create_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.plans.create(plan_object())


def test_valid_update_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "plan_code"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/plans/" + code,
        content=mock_response(),
    )
    response = client.plans.update(plan_object(), code)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.code == code
    assert response.invoice_display_name == "test plan 1"
    assert response.minimum_commitment.invoice_display_name == "Minimum commitment (C1)"


def test_invalid_update_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/plans/" + code,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.plans.update(plan_object(), code)


def test_valid_find_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "plan_code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + code,
        content=mock_response(),
    )
    response = client.plans.find(code)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.code == code
    assert response.invoice_display_name == "test plan 1"
    assert response.charges.__root__[0].charge_model == "standard"
    assert response.charges.__root__[0].min_amount_cents == 0
    assert response.minimum_commitment.amount_cents == 1000


def test_invalid_find_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.plans.find(code)


def test_valid_destroy_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    code = "plan_code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + code,
        content=mock_response(),
    )
    response = client.plans.destroy(code)

    assert response.lago_id == "b7ab2926-1de8-4428-9bcd-779314ac129b"
    assert response.code == code


def test_invalid_destroy_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    code = "invalid"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + code,
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.plans.destroy(code)


def test_valid_find_all_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans",
        content=mock_collection_response(),
    )
    response = client.plans.find_all()

    assert response["plans"][0].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1111"
    assert response["plans"][0].invoice_display_name == "test plan 1"
    assert response["plans"][0].minimum_commitment.invoice_display_name == "Minimum commitment (C2)"
    assert response["plans"][0].charges.__root__[0].lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"
    assert response["plans"][0].charges.__root__[0].filters.__root__[0].properties["amount"] == "0.22"
    assert response["plans"][0].charges.__root__[0].filters.__root__[0].invoice_display_name == "Europe"
    assert response["meta"]["current_page"] == 1


def test_valid_find_all_plan_request_with_options(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans?per_page=2&page=1",
        content=mock_collection_response(),
    )
    response = client.plans.find_all({"per_page": 2, "page": 1})

    assert response["plans"][1].lago_id == "b7ab2926-1de8-4428-9bcd-779314ac1222"
    assert response["meta"]["current_page"] == 1


def test_invalid_find_all_plan_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.plans.find_all()


def mock_metadata_response():
    return b'{"metadata": {"foo": "bar", "baz": null}}'


def mock_null_metadata_response():
    return b'{"metadata": null}'


def test_plan_with_fixed_charges_serialization():
    plan = plan_with_fixed_charges_object()
    plan_dict = plan.dict()

    assert plan_dict["name"] == "plan_with_fixed_charges"
    assert plan_dict["code"] == "plan_fixed"
    assert plan_dict["bill_fixed_charges_monthly"] is True
    # When serialized, __root__ models become lists directly
    assert plan_dict["fixed_charges"][0]["add_on_id"] == "add_on_123"
    assert plan_dict["fixed_charges"][0]["charge_model"] == "standard"
    assert plan_dict["fixed_charges"][0]["invoice_display_name"] == "Setup Fee"
    assert plan_dict["fixed_charges"][0]["units"] == 1.0
    assert plan_dict["fixed_charges"][0]["pay_in_advance"] is True
    assert plan_dict["fixed_charges"][0]["prorated"] is False
    assert plan_dict["fixed_charges"][0]["properties"]["amount"] == "500"


def test_valid_replace_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.plans.replace_metadata(plan_code, {"foo": "bar", "baz": None})

    assert response == {"foo": "bar", "baz": None}


def test_valid_merge_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="PATCH",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/metadata",
        content=mock_metadata_response(),
    )
    response = client.plans.merge_metadata(plan_code, {"foo": "qux"})

    assert response == {"foo": "bar", "baz": None}


def test_valid_delete_all_metadata_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/metadata",
        content=mock_null_metadata_response(),
    )
    response = client.plans.delete_all_metadata(plan_code)

    assert response is None


def test_valid_delete_metadata_key_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    key = "foo"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/metadata/" + key,
        content=b'{"metadata": {"baz": "qux"}}',
    )
    response = client.plans.delete_metadata_key(plan_code, key)

    assert response == {"baz": "qux"}


# --- Charges ---


def mock_plan_charge_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_charge.json")

    with open(data_path, "rb") as f:
        return f.read()


def mock_plan_charges_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_charges.json")

    with open(data_path, "rb") as f:
        return f.read()


def test_valid_find_all_charges_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges",
        content=mock_plan_charges_response(),
    )
    response = client.plans.find_all_charges(plan_code)

    assert len(response["charges"]) == 1
    assert response["charges"][0].lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"
    assert response["charges"][0].code == "charge_code"
    assert response["charges"][0].charge_model == "standard"
    assert response["meta"]["current_page"] == 1


def test_valid_find_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code,
        content=mock_plan_charge_response(),
    )
    response = client.plans.find_charge(plan_code, charge_code)

    assert response.lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"
    assert response.code == "charge_code"
    assert response.charge_model == "standard"
    assert response.invoice_display_name == "Setup"


def test_valid_create_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges",
        content=mock_plan_charge_response(),
    )
    charge = Charge(
        billable_metric_id="a6947936-628f-4945-8857-db6858ee7941",
        charge_model="standard",
        pay_in_advance=True,
        invoiceable=True,
        properties={"amount": "0.22"},
    )
    response = client.plans.create_charge(plan_code, charge)

    assert response.lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"
    assert response.charge_model == "standard"


def test_valid_update_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code,
        content=mock_plan_charge_response(),
    )
    charge = Charge(invoice_display_name="Updated Setup")
    response = client.plans.update_charge(plan_code, charge_code, charge)

    assert response.lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"


def test_valid_destroy_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code,
        content=mock_plan_charge_response(),
    )
    response = client.plans.destroy_charge(plan_code, charge_code)

    assert response.lago_id == "51c1e851-5be6-4343-a0ee-39a81d8b4ee1"


# --- Fixed Charges ---


def mock_plan_fixed_charge_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_fixed_charge.json")

    with open(data_path, "rb") as f:
        return f.read()


def mock_plan_fixed_charges_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_fixed_charges.json")

    with open(data_path, "rb") as f:
        return f.read()


def test_valid_find_all_fixed_charges_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/fixed_charges",
        content=mock_plan_fixed_charges_response(),
    )
    response = client.plans.find_all_fixed_charges(plan_code)

    assert len(response["fixed_charges"]) == 1
    assert response["fixed_charges"][0].lago_id == "fc901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["fixed_charges"][0].charge_model == "standard"
    assert response["fixed_charges"][0].invoice_display_name == "Setup Fee"
    assert response["meta"]["current_page"] == 1


def test_valid_find_fixed_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    fixed_charge_code = "fixed_setup"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/fixed_charges/" + fixed_charge_code,
        content=mock_plan_fixed_charge_response(),
    )
    response = client.plans.find_fixed_charge(plan_code, fixed_charge_code)

    assert response.lago_id == "fc901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.add_on_code == "setup_fee"
    assert response.charge_model == "standard"
    assert response.properties.amount == "500"


def test_valid_create_fixed_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/fixed_charges",
        content=mock_plan_fixed_charge_response(),
    )
    fixed_charge = FixedCharge(
        add_on_id="ao901a90-1a90-1a90-1a90-1a901a901a90",
        charge_model="standard",
        invoice_display_name="Setup Fee",
        units=1.0,
        properties=FixedChargeProperties(amount="500"),
    )
    response = client.plans.create_fixed_charge(plan_code, fixed_charge)

    assert response.lago_id == "fc901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.charge_model == "standard"


def test_valid_update_fixed_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    fixed_charge_code = "fixed_setup"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/fixed_charges/" + fixed_charge_code,
        content=mock_plan_fixed_charge_response(),
    )
    fixed_charge = FixedCharge(invoice_display_name="Updated Setup Fee")
    response = client.plans.update_fixed_charge(plan_code, fixed_charge_code, fixed_charge)

    assert response.lago_id == "fc901a90-1a90-1a90-1a90-1a901a901a90"


def test_valid_destroy_fixed_charge_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    fixed_charge_code = "fixed_setup"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/fixed_charges/" + fixed_charge_code,
        content=mock_plan_fixed_charge_response(),
    )
    response = client.plans.destroy_fixed_charge(plan_code, fixed_charge_code)

    assert response.lago_id == "fc901a90-1a90-1a90-1a90-1a901a901a90"


# --- Charge Filters ---


def mock_plan_charge_filter_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_charge_filter.json")

    with open(data_path, "rb") as f:
        return f.read()


def mock_plan_charge_filters_response():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(this_dir, "fixtures/plan_charge_filters.json")

    with open(data_path, "rb") as f:
        return f.read()


def test_valid_find_all_charge_filters_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code + "/filters",
        content=mock_plan_charge_filters_response(),
    )
    response = client.plans.find_all_charge_filters(plan_code, charge_code)

    assert len(response["filters"]) == 1
    assert response["filters"][0].lago_id == "f1901a90-1a90-1a90-1a90-1a901a901a90"
    assert response["filters"][0].invoice_display_name == "From France"
    assert response["meta"]["current_page"] == 1


def test_valid_find_charge_filter_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"
    filter_id = "f1901a90-1a90-1a90-1a90-1a901a901a90"

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code + "/filters/" + filter_id,
        content=mock_plan_charge_filter_response(),
    )
    response = client.plans.find_charge_filter(plan_code, charge_code, filter_id)

    assert response.lago_id == "f1901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.invoice_display_name == "From France"
    assert response.values == {"country": ["France"]}


def test_valid_create_charge_filter_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code + "/filters",
        content=mock_plan_charge_filter_response(),
    )
    filter_input = ChargeFilter(
        invoice_display_name="From France",
        properties={"amount": "0.33"},
        values={"country": ["France"]},
    )
    response = client.plans.create_charge_filter(plan_code, charge_code, filter_input)

    assert response.lago_id == "f1901a90-1a90-1a90-1a90-1a901a901a90"
    assert response.invoice_display_name == "From France"


def test_valid_update_charge_filter_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"
    filter_id = "f1901a90-1a90-1a90-1a90-1a901a901a90"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code + "/filters/" + filter_id,
        content=mock_plan_charge_filter_response(),
    )
    filter_input = ChargeFilter(invoice_display_name="Updated France")
    response = client.plans.update_charge_filter(plan_code, charge_code, filter_id, filter_input)

    assert response.lago_id == "f1901a90-1a90-1a90-1a90-1a901a901a90"


def test_valid_destroy_charge_filter_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    plan_code = "plan_code"
    charge_code = "charge_code"
    filter_id = "f1901a90-1a90-1a90-1a90-1a901a901a90"

    httpx_mock.add_response(
        method="DELETE",
        url="https://api.getlago.com/api/v1/plans/" + plan_code + "/charges/" + charge_code + "/filters/" + filter_id,
        content=mock_plan_charge_filter_response(),
    )
    response = client.plans.destroy_charge_filter(plan_code, charge_code, filter_id)

    assert response.lago_id == "f1901a90-1a90-1a90-1a90-1a901a901a90"
