from coar_notify_validator.validate import validate
from coar_notify_validator.validate import InvalidNotificationType, MissingNotificationType


def validate_notification(notification: dict) -> tuple[bool, list[dict]]:
    try:
        return validate(notification)
    except InvalidNotificationType:
        return False, [{"message": "Invalid notification type."}]
    except MissingNotificationType:
        return False, [{"message": "Missing notification type."}]
