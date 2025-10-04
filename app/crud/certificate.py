import datetime
from pydantic import BaseModel
from volunteer import VolunteerModel
from template import CertificateTemplateModel


class CertificateModel(BaseModel):
    id: int
    volunteer_id: int
    template_id: int
    confirmed: bool
    issued_at: datetime.datetime
    volunteer: VolunteerModel
    template: CertificateTemplateModel
