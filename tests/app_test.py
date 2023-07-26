from fastapi.testclient import TestClient
from unittest.mock import patch

from app import app
from routers.inbox import INBOX_URL

client = TestClient(app)


def test_read_inbox_options():
    response = client.options("/inbox/")

    assert response.status_code == 200
    assert response.headers["Accept-Post"] == "application/ld+json"


@patch("routers.inbox.get_notifications")
def test_read_inbox(mock_get_notifications):
    mock_get_notifications.return_value = []

    response = client.get("/inbox/")

    assert response.status_code == 200
    assert response.json() == {
        "@context": "http://www.w3.org/ns/ldp",
        "@id": INBOX_URL,
        "contains": [],
    }


@patch("routers.inbox.create_notification")
def test_add_notification(mock_create_notification, valid_notification_payload):
    mock_create_notification.return_value = valid_notification_payload["id"]

    response = client.post("/inbox/", json=valid_notification_payload)

    assert response.status_code == 201
    assert response.headers["Location"] == f"{INBOX_URL}{valid_notification_payload['id']}"


@patch("routers.inbox.get_notification")
def test_read_notification(mock_get_notification, valid_notification_payload):
    mock_notification = {
        "updated": "2022-10-06T15:00:00.000000",
        **valid_notification_payload
    }

    mock_get_notification.return_value = mock_notification

    response = client.get(f"/inbox/{valid_notification_payload['id']}/")

    assert response.status_code == 200
    assert response.json() == mock_notification
