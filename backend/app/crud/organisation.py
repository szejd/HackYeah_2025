from user import UserModel
from domain import DomainModel

class OrganisationModel(UserModel):
    id: int
    user_id: int
    org_name: str
    contact_person: str
    description: str
    phone_number: str
    address: str
    verified: bool
    domains: list[DomainModel]