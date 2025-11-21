import os

import pytest
from pytest_httpx import HTTPXMock

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import BillingEntity, BillingEntityUpdate, BillingEntityBillingConfiguration


def mock_response(mock="billing_entity"):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    my_data_path = os.path.join(this_dir, "fixtures/" + mock + ".json")

    with open(my_data_path, "rb") as billing_entity_response:
        return billing_entity_response.read()


def create_billing_entity_input():
    return BillingEntity(
        name="Test Company",
        code="test-company",
        address_line1="123 Test Street",
        address_line2="Suite 100",
        city="Test City",
        state="TS",
        zipcode="12345",
        country="US",
        email="test@company.com",
        phone="+1234567890",
        default_currency="USD",
        timezone="UTC",
        document_numbering="per_customer",
        document_number_prefix="TEST-",
        finalize_zero_amount_invoice=True,
        net_payment_term=30,
        eu_tax_management=False,
        logo="=base64 encoded file",
        legal_name="Test Company Legal Name",
        legal_number="123456789",
        tax_identification_number="TAX123456",
        email_settings=["invoice.finalized", "payment_receipt.created"],
        billing_configuration=BillingEntityBillingConfiguration(
            invoice_footer="Thank you for your business",
            invoice_grace_period=3,
            subscription_invoice_issuing_date_anchor="current_period_end",
            subscription_invoice_issuing_date_adjustment="keep_anchor",
            document_locale="en",
        ),
    )


def update_billing_entity_input():
    return BillingEntityUpdate(
        name="Updated Company Name",
        address_line1="456 Test Avenue",
        address_line2="Suite 200",
        city="Updated City",
        state="Greater Paris",
        zipcode="54321",
        country="FR",
        email="updated@company.com",
        phone="+1987654321",
        default_currency="EUR",
        timezone="UTC",
        document_numbering="per_billing_entity",
        document_number_prefix="UPD-",
        finalize_zero_amount_invoice=True,
        net_payment_term=15,
        eu_tax_management=True,
        logo="=base 64 encoded file",
        legal_name="Updated Company Legal Name",
        legal_number="987654321",
        tax_identification_number="TAX654321",
        tax_codes=["VAT-01", "VAT-25"],
        email_settings=["invoice.finalized"],
        billing_configuration=BillingEntityBillingConfiguration(
            invoice_footer="Updated footer",
            invoice_grace_period=5,
            subscription_invoice_issuing_date_anchor="current_period_end",
            subscription_invoice_issuing_date_adjustment="keep_anchor",
            document_locale="fr",
        ),
        invoice_custom_section_codes=["custom_section_1", "custom_section_2"],
    )


def test_valid_create_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/billing_entities",
        content=mock_response(),
    )
    response = client.billing_entities.create(create_billing_entity_input())

    assert response is not None
    assert response.lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response.code == "test-company"


def test_invalid_create_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="POST",
        url="https://api.getlago.com/api/v1/billing_entities",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.billing_entities.create(create_billing_entity_input())


def test_valid_find_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/billing_entities/test-company",
        content=mock_response(),
    )
    response = client.billing_entities.find("test-company")

    assert response is not None
    assert response.lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response.code == "test-company"


def test_invalid_find_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/billing_entities/invalid-code",
        status_code=404,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.billing_entities.find("invalid-code")


def test_valid_find_all_billing_entities_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/billing_entities",
        content=mock_response("billing_entity_index"),
    )
    response = client.billing_entities.find_all()

    assert len(response["billing_entities"]) == 2
    assert response["meta"]["current_page"] == 1

    assert response["billing_entities"][0].lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response["billing_entities"][0].code == "test-company-1"
    assert response["billing_entities"][1].lago_id == "123e4567-e89b-12d3-a456-426614174001"
    assert response["billing_entities"][1].code == "test-company-2"


def test_invalid_find_all_billing_entities_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")

    httpx_mock.add_response(
        method="GET",
        url="https://api.getlago.com/api/v1/billing_entities",
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.billing_entities.find_all()


def test_valid_update_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="886fe239-927d-4072-ab72-6dd345e8dd0d")
    billing_entity_code = "test-company"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/billing_entities/" + billing_entity_code,
        content=mock_response(),
    )
    response = client.billing_entities.update(update_billing_entity_input(), billing_entity_code)

    assert response.lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response.code == "test-company"


def test_invalid_update_billing_entity_request(httpx_mock: HTTPXMock):
    client = Client(api_key="invalid")
    billing_entity_code = "test-company"

    httpx_mock.add_response(
        method="PUT",
        url="https://api.getlago.com/api/v1/billing_entities/" + billing_entity_code,
        status_code=401,
        content=b"",
    )

    with pytest.raises(LagoApiError):
        client.billing_entities.update(update_billing_entity_input(), billing_entity_code)
