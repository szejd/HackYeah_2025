from pydantic import BaseModel
from datetime import date
from volunteer import VolunteerModel
from template import CertificateTemplateModel
from datetime import date

class CertificateModel(BaseModel):
    id: int
    volunteer_id: int
    template_id: int
    confirmed: bool
    issued_at: date
    volunteer: VolunteerModel
    template: CertificateTemplateModel