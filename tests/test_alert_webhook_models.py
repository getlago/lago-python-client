import json

from lago_python_client.models import ResolvedAlert, TriggeredAlert

from .utils.mixin import mock_response


def triggered_alert_payload():
    return json.loads(mock_response("alert_triggered_webhook"))["triggered_alert"]


def resolved_alert_payload():
    return json.loads(mock_response("alert_resolved_webhook"))["resolved_alert"]


def test_triggered_alert_parsing():
    alert = TriggeredAlert.parse_obj(triggered_alert_payload())

    assert alert.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a91"
    assert alert.lago_organization_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert alert.lago_alert_id == "1a901a90-1a90-1a90-1a90-1a901a901a92"
    assert alert.lago_subscription_id == "1a901a90-1a90-1a90-1a90-1a901a901a93"
    assert alert.external_subscription_id == "sub_1234"
    assert alert.lago_wallet_id is None
    assert alert.external_customer_id == "cust_1234"
    assert alert.billable_metric_code == "storage"
    assert alert.alert_name == "Storage usage"
    assert alert.alert_code == "storage_alert"
    assert alert.alert_type == "billable_metric_current_usage_amount"
    assert alert.current_value == "25000.0"
    assert alert.previous_value == "5000.0"
    assert alert.triggered_at == "2026-10-28T12:00:00Z"
    assert alert.subscription_external_id == "sub_1234"
    assert alert.customer_external_id == "cust_1234"

    thresholds = alert.crossed_thresholds.__root__
    assert len(thresholds) == 2
    assert thresholds[0].code is None
    assert thresholds[0].value == "10000.0"
    assert type(thresholds[0].value) is str
    assert thresholds[0].recurring is False
    assert thresholds[1].code == "warn"
    assert thresholds[1].value == "20000.0"
    assert type(thresholds[1].value) is str
    assert thresholds[1].recurring is True


def test_triggered_alert_parsing_without_previous_value():
    payload = triggered_alert_payload()
    payload["previous_value"] = None

    alert = TriggeredAlert.parse_obj(payload)

    assert alert.previous_value is None
    assert alert.current_value == "25000.0"


def test_resolved_alert_parsing():
    alert = ResolvedAlert.parse_obj(resolved_alert_payload())

    assert alert.lago_id == "1a901a90-1a90-1a90-1a90-1a901a901a94"
    assert alert.lago_organization_id == "1a901a90-1a90-1a90-1a90-1a901a901a90"
    assert alert.lago_alert_id == "1a901a90-1a90-1a90-1a90-1a901a901a92"
    assert alert.lago_subscription_id == "1a901a90-1a90-1a90-1a90-1a901a901a93"
    assert alert.external_subscription_id == "sub_1234"
    assert alert.lago_wallet_id is None
    assert alert.external_customer_id == "cust_1234"
    assert alert.billable_metric_code == "storage"
    assert alert.alert_name == "Storage usage"
    assert alert.alert_code == "storage_alert"
    assert alert.alert_type == "billable_metric_current_usage_amount"
    assert alert.current_value == "15000.0"
    assert alert.previous_value == "25000.0"
    assert alert.in_alarm_thresholds == ["20000.0"]
    assert alert.fully_resolved is False
    assert alert.reason == "recovered"
    assert alert.resolved_at == "2026-10-28T13:00:00Z"

    thresholds = alert.recovered_thresholds.__root__
    assert len(thresholds) == 1
    assert thresholds[0].code is None
    assert thresholds[0].value == "10000.0"
    assert type(thresholds[0].value) is str
    assert thresholds[0].recurring is False


def test_resolved_alert_parsing_without_previous_value():
    payload = resolved_alert_payload()
    payload["previous_value"] = None

    alert = ResolvedAlert.parse_obj(payload)

    assert alert.previous_value is None
    assert alert.fully_resolved is False
