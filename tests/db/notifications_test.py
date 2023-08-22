from unittest.mock import AsyncMock, patch

import pytest

from db.models import Notification
from db.notifications import (
    create_notification,
    get_notification,
    get_notifications,
    delete_notification,
)


@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_create_notification(mock_get_collection, valid_notification_payload):
    mock_get_collection.return_value = AsyncMock()
    notification_input = Notification(**valid_notification_payload)

    notification_id = await create_notification(notification_input)

    assert mock_get_collection.call_count == 2
    assert mock_get_collection.return_value.insert_one.call_count == 2
    assert isinstance(notification_id, str)


@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_get_notification(mock_get_collection, notification_id):
    mock_get_collection.return_value = AsyncMock()

    _ = await get_notification(notification_id)

    mock_get_collection.assert_called_once()
    mock_get_collection.return_value.find_one.assert_called_once()


@patch('db.notifications.get_collection')
@pytest.mark.asyncio
@pytest.mark.skip(reason="Need to rework mocks")
async def test_get_notifications(mock_get_collection):
    mock_collection = AsyncMock()
    mock_collection.find.return_value = AsyncMock()
    mock_get_collection.return_value = mock_collection

    mock_collection.find.return_value.sort.return_value.to_list.return_value = []

    notifications = await get_notifications()

    mock_collection.find.assert_called_once_with({}, {"_id": 0})
    mock_collection.find.return_value.sort.assert_called_once_with("updated", -1)
    mock_collection.find.return_value.sort.return_value.to_list.assert_called_once_with(length=100)
    assert notifications == []


@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_delete_notification(mock_get_collection, notification_id):
    mock_get_collection.return_value = AsyncMock()

    await delete_notification(notification_id)

    mock_get_collection.assert_called_once()
    mock_get_collection.return_value.delete_one.assert_called_once()
