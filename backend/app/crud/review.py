from pydantic import BaseModel
from datetime import date
from volunteer import VolunteerModel

class ReviewModel(BaseModel):
    id: int
    volunteer_id: int
    rating: int
    comment: str
    created_at: date
    volunteer: VolunteerModel