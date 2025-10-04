from pydantic import BaseModel
from datetime import date
from message import MessageModel

from app.models.user import UserResponse


class ChatModel(BaseModel):
    id: int
    created_at: date
    user: list[UserResponse]
    messages = list[MessageModel]
