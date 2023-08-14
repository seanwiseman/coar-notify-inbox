from unittest.mock import patch

from fastapi.testclient import TestClient


@patch("routers.notification_state.update_notification_state")
def test_add_notification_succeeds_when_valid_and_admin(mock_update_notification_state,
                                                        admin_client: TestClient):
    mock_notification_id = "1234-5678-9012-3456"
    payload = {"read": True}

    response = admin_client.patch(
        f"/notification_state/{mock_notification_id}",
        json=payload
    )

    assert response.status_code == 200
    assert mock_update_notification_state.call_count == 1
    assert mock_update_notification_state.call_args.args == (mock_notification_id, True)


@patch("routers.notification_state.update_notification_state")
def test_add_notification_fails_when_valid_but_non_admin(mock_update_notification_state,
                                                         client: TestClient):
    mock_notification_id = "1234-5678-9012-3456"
    payload = {"read": True}

    response = client.patch(
        f"/notification_state/{mock_notification_id}",
        json=payload
    )

    assert response.status_code == 403
    assert mock_update_notification_state.call_count == 0
