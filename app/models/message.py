from pydantic import BaseModel
from datetime import date
from chat import ChatModel
from app.models.user import UserResponse


class MessageModel(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    sent_at: date
    chat: ChatModel
    sender: UserResponse
