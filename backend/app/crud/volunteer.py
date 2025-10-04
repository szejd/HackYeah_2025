from user import UserModel
from datetime import date
from skill import SkillModel
from domain import DomainModel
from review import ReviewModel
from certificate import CertificateModel

class VolunteerModel(UserModel):
    first_name: str
    last_name: str
    birth_date: date
    phone_number: str
    skills: list[SkillModel]
    domains: list[DomainModel]
    reviews: list[ReviewModel]
    certificates: list[CertificateModel]