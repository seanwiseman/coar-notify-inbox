from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from routers.middleware import ensure_client_is_admin


@patch("routers.middleware.get_settings")
def test_ensure_client_is_admin_allows_ip_if_wildcard_configured(mock_get_settings):
    mock_get_settings.return_value.allowed_admin_origins = {"*"}

    mock_request = Mock()
    mock_request.client.host = "127.0.0.1"

    assert ensure_client_is_admin(mock_request) is None


@patch("routers.middleware.get_settings")
def test_ensure_client_is_admin_allows_admin_ip(mock_get_settings):
    mock_get_settings.return_value.allowed_admin_origins = {"127.0.0.1"}

    mock_request = Mock()
    mock_request.client.host = "127.0.0.1"

    assert ensure_client_is_admin(mock_request) is None


@patch("routers.middleware.get_settings")
def test_ensure_client_is_admin_rejects_non_admin_ip(mock_get_settings):
    mock_get_settings.return_value.allowed_admin_origins = {"127.0.0.1"}

    mock_request = Mock()
    mock_request.client.host = "10.0.0.1"

    with pytest.raises(HTTPException) as exc_info:
        ensure_client_is_admin(mock_request)

    assert exc_info.value.status_code == 403
    assert str(exc_info.value.detail) == "Access forbidden: IP not allowed"
