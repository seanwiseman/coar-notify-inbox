from datetime import datetime
from typing import Optional
from typing_extensions import TypedDict


ActorResource = TypedDict(
    "ActorResource",
    {
        "id": str,
        "type": str,
        "name": str,
    },
)


InboxResource = TypedDict(
    "InboxResource",
    {
        "id": str,
        "type": str,
        "inbox": str,
    },
)


DocumentObject = TypedDict(
    "DocumentObject",
    {
        "id": str,
        "type": Optional[list[str]],
        "ietf:cite-as": Optional[str],
    },
)


ContextObject = TypedDict(
    "ContextObject",
    {
        "id": str,
    },
)


Notification = TypedDict(
    "Notification",
    {
        "received_at": datetime,
        "id": str,
        "@context": list[str],
        "type": list[str],
        "origin": InboxResource,
        "target": InboxResource,
        "object": DocumentObject,
        "actor": ActorResource,
        "context": ContextObject,
    },
)

NotificationInput = TypedDict(
    "NotificationInput",
    {
        "id": str,
        "@context": list[str],
        "type": list[str],
        "origin": InboxResource,
        "target": InboxResource,
        "object": DocumentObject,
        "actor": ActorResource,
        "context": ContextObject,
    },
)
