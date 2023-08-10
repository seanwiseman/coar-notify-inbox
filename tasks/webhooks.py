import json
import logging
import requests

from db.models import Notification


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_notification_to_webhook(notification: Notification, webhook_url: str) -> None:
    try:
        response = requests.post(
            url=webhook_url,
            headers={"content-type": "application/ld+json"},
            json=json.dumps(notification, default=str),
            timeout=(10, 10),
        )

        response.raise_for_status()

        logger.info(f"Successfully sent notification to {webhook_url}. "
                    f"Status code: {response.status_code}")
    except requests.RequestException:
        logger.exception(f"Failed to send notification to {webhook_url}")
