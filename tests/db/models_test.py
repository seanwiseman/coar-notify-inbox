from db.models import Notification


def test_notification(valid_notification_payload):
    notification = Notification(**valid_notification_payload)
    assert notification.id


def test_notification_provides_default_updated_value(valid_notification_payload):
    notification = Notification(**valid_notification_payload)
    assert notification.updated


def test_notification_handles_at_context_alias(valid_notification_payload):
    notification = Notification(**valid_notification_payload)
    assert notification.at_context == valid_notification_payload["@context"]


def test_notification_handles_ietf_cite_as_alias(valid_notification_payload):
    notification = Notification(**valid_notification_payload)
    assert (notification.object.ietf_cite_as ==
            valid_notification_payload["object"]["ietf:cite-as"])
