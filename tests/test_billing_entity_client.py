import os

import pytest
from pytest_httpx import HTTPXMock
from datetime import datetime, timezone

from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import BillingEntity, BillingEntityUpdate, BillingEntityBillingConfiguration

def billing_entity_object():
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
        document_numbering="sequential",
        document_number_prefix="TEST-",
        finalize_zero_amount_invoice=True,
        net_payment_term=30,
        eu_tax_management=False,
        logo_url="https://example.com/logo.png",
        legal_name="Test Company Legal Name",
        legal_number="123456789",
        tax_identification_number="TAX123456",
        tax_codes=["VAT", "GST"],
        email_settings=["invoice.finalized"],
        billing_configuration=BillingEntityBillingConfiguration(
            invoice_footer="Thank you for your business",
            invoice_grace_period=3,
            document_locale="en",
        ),
    )


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
        document_numbering="sequential",
        document_number_prefix="TEST-",
        finalize_zero_amount_invoice=True,
        net_payment_term=30,
        eu_tax_management=False,
        logo_url="https://example.com/logo.png",
        legal_name="Test Company Legal Name",
        legal_number="123456789",
        tax_identification_number="TAX123456",
        email_settings=["invoice.finalized", "payment_receipt.created"],
        billing_configuration=BillingEntityBillingConfiguration(
            invoice_footer="Thank you for your business",
            invoice_grace_period=3,
            document_locale="en",
        ),
    )


def update_billing_entity_input():
    return BillingEntityUpdate(
        name="Updated Company Name",
        address_line1="456 Test Avenue",
        address_line2="Suite 200",
        city="Updated City",
        state="US",
        zipcode="54321",
        country="US",
        email="updated@company.com",
        phone="+1987654321",
        default_currency="EUR",
        timezone="UTC",
        document_numbering="sequential",
        document_number_prefix="UPD-",
        finalize_zero_amount_invoice=True,
        net_payment_term=15,
        eu_tax_management=True,
        logo_url="https://example.com/updated-logo.png",
        legal_name="Updated Company Legal Name",
        legal_number="987654321",
        tax_identification_number="TAX654321",
        tax_codes=["VAT"],
        email_settings=["invoice.finalized"],
        billing_configuration=BillingEntityBillingConfiguration(
            invoice_footer="Updated footer",
            invoice_grace_period=5,
            document_locale="fr",
        ),
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
    assert response.name == "Test Company"
    assert response.address_line1 == "123 Test Street"
    assert response.address_line2 == "Suite 100"
    assert response.city == "Test City"
    assert response.state == "TS"
    assert response.zipcode == "12345"
    assert response.country == "US"
    assert response.email == "test@company.com"
    assert response.phone == "+1234567890"
    assert response.default_currency == "USD"
    assert response.timezone == "UTC"
    assert response.document_numbering == "sequential"
    assert response.document_number_prefix == "TEST-"
    assert response.finalize_zero_amount_invoice is True
    assert response.net_payment_term == 30
    assert response.eu_tax_management is False
    assert response.logo_url == "https://example.com/logo.png"
    assert response.legal_name == "Test Company Legal Name"
    assert response.legal_number == "123456789"
    assert response.tax_identification_number == "TAX123456"
    assert response.tax_codes == ["VAT", "GST"]
    assert response.email_settings == ["invoice.finalized", "payment_receipt.created"]
    assert response.billing_configuration.invoice_footer == "Thank you for your business"
    assert response.billing_configuration.invoice_grace_period == 3
    assert response.billing_configuration.document_locale == "en"
    assert response.created_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)
    assert response.updated_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)


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

    assert response.lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response.code == "test-company"
    assert response.name == "Test Company"
    assert response.address_line1 == "123 Test Street"
    assert response.address_line2 == "Suite 100"
    assert response.city == "Test City"
    assert response.state == "TS"
    assert response.zipcode == "12345"
    assert response.country == "US"
    assert response.email == "test@company.com"
    assert response.phone == "+1234567890"
    assert response.default_currency == "USD"
    assert response.timezone == "UTC"
    assert response.document_numbering == "sequential"
    assert response.document_number_prefix == "TEST-"
    assert response.finalize_zero_amount_invoice is True
    assert response.net_payment_term == 30
    assert response.eu_tax_management is False
    assert response.logo_url == "https://example.com/logo.png"
    assert response.legal_name == "Test Company Legal Name"
    assert response.legal_number == "123456789"
    assert response.tax_identification_number == "TAX123456"
    assert response.tax_codes == ["VAT", "GST"]
    assert response.email_settings == ["invoice.finalized", "payment_receipt.created"]
    assert response.billing_configuration.invoice_footer == "Thank you for your business"
    assert response.billing_configuration.invoice_grace_period == 3
    assert response.billing_configuration.document_locale == "en"
    assert response.created_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)
    assert response.updated_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)


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
    
    assert response["billing_entities"][0].lago_id == "123e4567-e89b-12d3-a456-426614174000"
    assert response["billing_entities"][0].code == "test-company-1"
    assert response["billing_entities"][0].name == "Test Company 1"
    assert response["billing_entities"][0].address_line1 == "123 Test Street"
    assert response["billing_entities"][0].address_line2 == "Suite 100"
    assert response["billing_entities"][0].city == "Test City"
    assert response["billing_entities"][0].state == "TS"
    assert response["billing_entities"][0].zipcode == "12345"
    assert response["billing_entities"][0].country == "US"
    assert response["billing_entities"][0].email == "test1@company.com"
    assert response["billing_entities"][0].phone == "+1234567890"
    assert response["billing_entities"][0].default_currency == "USD"
    assert response["billing_entities"][0].timezone == "UTC"
    assert response["billing_entities"][0].document_numbering == "sequential"
    assert response["billing_entities"][0].document_number_prefix == "TEST1-"
    assert response["billing_entities"][0].finalize_zero_amount_invoice is True
    assert response["billing_entities"][0].net_payment_term == 30
    assert response["billing_entities"][0].eu_tax_management is False
    assert response["billing_entities"][0].logo_url == "https://example.com/logo.png"
    assert response["billing_entities"][0].legal_name == "Test Company 1 Legal Name"
    assert response["billing_entities"][0].legal_number == "123456789"
    assert response["billing_entities"][0].tax_identification_number == "TAX123456"
    assert response["billing_entities"][0].tax_codes == ["VAT", "GST"]
    assert response["billing_entities"][0].email_settings == ["invoice.finalized", "payment_receipt.created"]
    assert response["billing_entities"][0].billing_configuration.invoice_footer == "Thank you for your business"
    assert response["billing_entities"][0].billing_configuration.invoice_grace_period == 3
    assert response["billing_entities"][0].billing_configuration.document_locale == "en"
    assert response["billing_entities"][1].created_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)
    assert response["billing_entities"][1].updated_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)

    assert response["billing_entities"][1].lago_id == "123e4567-e89b-12d3-a456-426614174001"
    assert response["billing_entities"][1].code == "test-company-2"
    assert response["billing_entities"][1].name == "Test Company 2"
    assert response["billing_entities"][1].address_line1 == "456 Test Avenue"
    assert response["billing_entities"][1].address_line2 == "Suite 200"
    assert response["billing_entities"][1].city == "Test City"
    assert response["billing_entities"][1].state == "TS"
    assert response["billing_entities"][1].zipcode == "12345"
    assert response["billing_entities"][1].country == "FR"
    assert response["billing_entities"][1].email == "test2@company.com"
    assert response["billing_entities"][1].phone == "+1987654321"
    assert response["billing_entities"][1].default_currency == "EUR"
    assert response["billing_entities"][1].timezone == "UTC"
    assert response["billing_entities"][1].document_numbering == "sequential"
    assert response["billing_entities"][1].document_number_prefix == "TEST2-"
    assert response["billing_entities"][1].finalize_zero_amount_invoice is True
    assert response["billing_entities"][1].net_payment_term == 30
    assert response["billing_entities"][1].eu_tax_management is True
    assert response["billing_entities"][1].logo_url == "https://example.com/logo_2.png"
    assert response["billing_entities"][1].legal_name == "Test Company 2 Legal Name"
    assert response["billing_entities"][1].legal_number == "987654321"
    assert response["billing_entities"][1].tax_identification_number == "TAX654321"
    assert response["billing_entities"][1].tax_codes == ["VAT"]
    assert response["billing_entities"][1].email_settings == ["invoice.finalized"]
    assert response["billing_entities"][1].billing_configuration.invoice_footer == "Thank you for your business"
    assert response["billing_entities"][1].billing_configuration.invoice_grace_period == 3
    assert response["billing_entities"][1].billing_configuration.document_locale == "fr"
    assert response["billing_entities"][1].created_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)
    assert response["billing_entities"][1].updated_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)


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
    assert response.name == "Test Company"
    assert response.address_line1 == "123 Test Street"
    assert response.address_line2 == "Suite 100"
    assert response.city == "Test City"
    assert response.state == "TS"
    assert response.zipcode == "12345"
    assert response.country == "US"
    assert response.email == "test@company.com"
    assert response.phone == "+1234567890"
    assert response.default_currency == "USD"
    assert response.timezone == "UTC"
    assert response.document_numbering == "sequential"
    assert response.document_number_prefix == "TEST-"
    assert response.finalize_zero_amount_invoice is True
    assert response.net_payment_term == 30
    assert response.eu_tax_management is False
    assert response.logo_url == "https://example.com/logo.png"
    assert response.legal_name == "Test Company Legal Name"
    assert response.legal_number == "123456789"
    assert response.tax_identification_number == "TAX123456"
    assert response.tax_codes == ["VAT", "GST"]
    assert response.email_settings == ["invoice.finalized", "payment_receipt.created"]
    assert response.billing_configuration.invoice_footer == "Thank you for your business"
    assert response.billing_configuration.invoice_grace_period == 3
    assert response.billing_configuration.document_locale == "en"
    assert response.created_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)
    assert response.updated_at == datetime(2024, 3, 20, 10, 0, tzinfo=timezone.utc)


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