from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ActorResource(BaseModel):
    id: str
    type: str
    name: str


class InboxResource(BaseModel):
    id: str
    type: str
    inbox: str


class DocumentObject(BaseModel):
    id: str
    object: Optional[str] = None
    type: Optional[List[str]] = None
    ietf_cite_as: Optional[str] = Field(alias="ietf:cite-as", default=None)


class ContextObject(BaseModel):
    id: str


class Notification(BaseModel):
    id: str
    updated: Optional[datetime] = Field(default_factory=datetime.utcnow)
    at_context: List[str] = Field(alias="@context")
    type: List[str]
    origin: InboxResource
    target: InboxResource
    object: DocumentObject
    actor: ActorResource
    context: ContextObject

    class Config:
        use_alias = True
        populate_by_name = True


class NotificationState(BaseModel):
    id: str
    read: bool
