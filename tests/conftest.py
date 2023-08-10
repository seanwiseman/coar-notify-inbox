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


@pytest.fixture
def invalid_notification_payload():
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
            # Missing inbox key
            "type": "Service"
        },
        "type": [
            "Announce",
            "coar-notify:ReviewAction"
        ]
    }


@pytest.fixture
def valid_offer_review_payload():
    return {
        "@context": [
            "https://www.w3.org/ns/activitystreams",
            "https://purl.org/coar/notify"
        ],
        "actor": {
            "id": "https://orcid.org/0000-0002-1825-0097",
            "name": "Josiah Carberry",
            "type": "Person"
        },
        "id": "urn:uuid:0370c0fb-bb78-4a9b-87f5-bed307a509dd",
        "object": {
            "id": "https://research.org/repository/preprint/201203/421/",
            "ietf:cite-as": "https://doi.org/10.5555/12345680",
            "type": "sorg:AboutPage",
            "url": {
                "id": "https://research.org/repository/preprint/201203/421/content.pdf",
                "mediaType": "application/pdf",
                "type": [
                    "Article",
                    "sorg:ScholarlyArticle"
                ]
            }
        },
        "origin": {
            "id": "https://research.org/repository",
            "inbox": "https://research.org/inbox/",
            "type": "Service"
        },
        "target": {
            "id": "https://review-service.com/system",
            "inbox": "https://review-service.com/inbox/",
            "type": "Service"
        },
        "type": [
            "Offer",
            "coar-notify:ReviewAction"
        ]
    }
