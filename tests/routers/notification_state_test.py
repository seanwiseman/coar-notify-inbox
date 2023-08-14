from unittest.mock import patch

from fastapi.testclient import TestClient


@patch("routers.notification_state.update_notification_state")
def test_add_notification_succeeds_when_valid_and_admin(mock_update_notification_state,
                                                        admin_client: TestClient):
    mock_notification_id = "1234-5678-9012-3456"
    payload = {"read": True}

    response = admin_client.patch(
        f"/notification_states/{mock_notification_id}",
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
        f"/notification_states/{mock_notification_id}",
        json=payload
    )

    assert response.status_code == 403
    assert mock_update_notification_state.call_count == 0


@patch("routers.notification_state.get_notification_state_ids_by_status")
def test_get_notification_states_succeeds_when_valid_and_admin(
        mock_get_notification_state_ids_by_status,
        admin_client: TestClient
):
    mock_get_notification_state_ids_by_status.return_value = ["1234-5678-9012-3456"]
    response = admin_client.get(f"/notification_states/?read={True}")

    assert response.status_code == 200
    assert mock_get_notification_state_ids_by_status.call_count == 1
    assert mock_get_notification_state_ids_by_status.call_args[0][0]
