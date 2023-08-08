from coar_notify_validator.validate import validate


def validate_notification(notification: dict) -> tuple[bool, list[dict]]:
    validate_payload = {
        **notification,
        # "updated": notification.get("updated", ).isoformat(),
    }
    return validate(validate_payload)
