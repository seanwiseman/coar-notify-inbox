import pytest
from validation.validate import validate_notification


@pytest.mark.skip(reason="Skipping until coar_notify_validator is fixed")
def test_validate_notification_success(valid_notification_payload):
    is_valid, errors = validate_notification(valid_notification_payload)
    assert is_valid
    assert not errors


@pytest.mark.skip(reason="Skipping until coar_notify_validator is fixed")
def test_validate_notification_failure(invalid_notification_payload):
    is_valid, errors = validate_notification(invalid_notification_payload)
    assert not is_valid
    assert errors
    assert len(errors) == 1


@pytest.mark.skip(reason="Skipping until coar_notify_validator is fixed")
def test_validate_notification_raises_on_invalid_type(valid_notification_payload):
    payload = {**valid_notification_payload, "type": "invalid"}

    is_valid, errors = validate_notification(payload)
    assert not is_valid
    assert errors
    assert len(errors) == 1
    assert errors[0]["message"] == "Invalid notification type."


@pytest.mark.skip(reason="Skipping until coar_notify_validator is fixed")
def test_validate_notification_raises_on_missing_type(valid_notification_payload):
    payload = {**valid_notification_payload}
    del payload["type"]

    is_valid, errors = validate_notification(payload)
    assert not is_valid
    assert errors
    assert len(errors) == 1
    assert errors[0]["message"] == "Missing notification type."


@pytest.mark.skip(reason="Skipping until coar_notify_validator is fixed")
def test_validate_offer_review_payload(valid_offer_review_payload):
    is_valid, errors = validate_notification(valid_offer_review_payload)
    assert is_valid
    assert not errors
