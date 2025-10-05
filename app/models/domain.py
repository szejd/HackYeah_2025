from pydantic import BaseModel
from app.models.user import UserResponse


class DomainModel(BaseModel):
    id: int
    name: str
    description: str | None = None
    users: list[UserResponse]
