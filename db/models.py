from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field


class ActorResource(BaseModel):
    id: str
    type: Union[list[str], str]
    name: Union[list[str], str]


class InboxResource(BaseModel):
    id: str
    inbox: str
    type: Union[list[str], str]


class UrlObject(BaseModel):
    id: str
    media_type: Optional[str] = Field(alias="mediaType", default=None)
    type: Optional[Union[list[str], str]] = None


class DocumentObject(BaseModel):
    id: str
    object: Optional[str] = None
    type: Union[list[str], str] = None
    ietf_cite_as: Optional[str] = Field(alias="ietf:cite-as", default=None)
    url: Optional[UrlObject] = None


class ContextObject(BaseModel):
    id: str
    ietf_cite_as: Optional[str] = Field(alias="ietf:cite-as", default=None)
    type: Union[list[str], str] = None


class Notification(BaseModel):
    id: str
    updated: Optional[datetime] = Field(default_factory=datetime.utcnow)
    at_context: list[str] = Field(alias="@context")
    type: Union[list[str], str]
    origin: InboxResource
    target: InboxResource
    object: DocumentObject
    actor: Optional[ActorResource] = None
    context: Optional[ContextObject] = None
    in_reply_to: Optional[str] = Field(alias="inReplyTo", default=None)

    class Config:
        use_alias = True
        populate_by_name = True


class NotificationState(BaseModel):
    id: str
    read: bool


class NotificationStateUpdatePayload(BaseModel):
    read: bool
