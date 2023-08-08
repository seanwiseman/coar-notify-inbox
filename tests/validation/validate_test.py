from validation.validate import validate_notification


def test_validate_notification_success(valid_notification_payload):
    is_valid, errors = validate_notification(valid_notification_payload)
    assert is_valid
    assert not errors


def test_validate_notification_failure(invalid_notification_payload):
    is_valid, errors = validate_notification(invalid_notification_payload)
    assert not is_valid
    assert errors
    assert len(errors) == 1
