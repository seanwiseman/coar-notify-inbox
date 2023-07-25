import pytest
from unittest.mock import AsyncMock, patch
from db.models import Notification, NotificationInput
from db.notifications import create_notification, get_notification, get_notifications, delete_notification


@patch('db.notifications.get_db')
@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_create_notification(mock_get_collection, mock_get_db, valid_notification_payload):
    mock_get_collection.return_value = AsyncMock()
    mock_get_db.return_value = AsyncMock()
    notification_input = NotificationInput(**valid_notification_payload)

    notification_id = await create_notification(notification_input)

    mock_get_db.assert_called_once()
    mock_get_collection.assert_called_once()
    mock_get_collection.return_value.insert_one.assert_called_once()
    assert isinstance(notification_id, str)


@patch('db.notifications.get_db')
@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_get_notification(mock_get_collection, mock_get_db, notification_id):
    mock_get_collection.return_value = AsyncMock()
    mock_get_db.return_value = AsyncMock()

    _ = await get_notification(notification_id)

    mock_get_db.assert_called_once()
    mock_get_collection.assert_called_once()
    mock_get_collection.return_value.find_one.assert_called_once()


@patch('db.notifications.get_db')
@patch('db.notifications.get_collection')
@pytest.mark.asyncio
@pytest.mark.skip(reason="Need to re work mocks")
async def test_get_notifications(mock_get_collection, mock_get_db):
    mock_collection = AsyncMock()
    mock_collection.find.return_value = AsyncMock()
    mock_get_collection.return_value = mock_collection
    mock_get_db.return_value = AsyncMock()

    mock_collection.find.return_value.sort.return_value.to_list.return_value = []

    notifications = await get_notifications()

    mock_get_db.assert_called_once()
    mock_get_collection.assert_called_once_with(mock_get_db.return_value, 'notifications')
    mock_collection.find.assert_called_once_with({}, {"_id": 0})
    mock_collection.find.return_value.sort.assert_called_once_with("received_at", -1)
    mock_collection.find.return_value.sort.return_value.to_list.assert_called_once_with(length=100)
    assert notifications == []


@patch('db.notifications.get_db')
@patch('db.notifications.get_collection')
@pytest.mark.asyncio
async def test_delete_notification(mock_get_collection, mock_get_db, notification_id):
    mock_get_collection.return_value = AsyncMock()
    mock_get_db.return_value = AsyncMock()

    await delete_notification(notification_id)

    mock_get_db.assert_called_once()
    mock_get_collection.assert_called_once()
    mock_get_collection.return_value.delete_one.assert_called_once()