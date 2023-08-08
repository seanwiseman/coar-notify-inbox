from coar_notify_validator.validate import validate

from db.models import Notification


def validate_notification(notification: Notification) -> tuple[bool, list[dict]]:
    validate_payload = {
        **notification.model_dump(by_alias=True),
        "updated": notification.updated.isoformat(),
    }
    return validate(validate_payload)
