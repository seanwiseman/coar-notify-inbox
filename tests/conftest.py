import pytest


@pytest.fixture
def notification_id():
    return "urn:uuid:049a719d-cb3a-4efe-ba82-77c68847dddf"


@pytest.fixture
def valid_notification_payload():
    return {
            "id": "urn:uuid:049a719d-cb3a-4efe-ba82-77c68847dddf",
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://purl.org/coar/notify"
            ],
            "actor": {
                "id": "https://sandbox.prereview.org/",
                "name": "PREreview",
                "type": "Service"
            },
            "context": {
                "id": "https://doi.org/10.1101/2022.10.06.511170"
            },
            "object": {
                "id": "https://sandbox.prereview.org/reviews/1224464",
                "ietf:cite-as": "10.5072/zenodo.1224464",
                "type": [
                    "Document",
                    "sorg:Review"
                ]
            },
            "origin": {
                "id": "https://sandbox.prereview.org/",
                "inbox": "https://sandbox.prereview.org/inbox",
                "type": "Service"
            },
            "target": {
                "id": "https://bioxriv.org/",
                "inbox": "http://notify-inbox.info/inbox",
                "type": "Service"
            },
            "type": [
                "Announce",
                "coar-notify:ReviewAction"
            ]
        }
