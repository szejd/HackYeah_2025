from pydantic import BaseModel
from datetime import date
from chat import ChatModel
from user import UserModel

class MessageModel(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    content: str
    sent_at: date
    chat: ChatModel
    sender: UserModel
