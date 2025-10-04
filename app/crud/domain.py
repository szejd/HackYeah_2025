from pydantic import BaseModel
from user import UserModel

class DomainModel(BaseModel):
    id: int
    name: str
    description: str = None
    users: list[UserModel]