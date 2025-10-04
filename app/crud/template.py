from pydantic import BaseModel

from app.crud.event import EventModel
from certificate import CertificateModel


class CertificateTemplateModel(BaseModel):
    id: int
    name: str
    content: str
    certificates: list[CertificateModel]
    event: EventModel
