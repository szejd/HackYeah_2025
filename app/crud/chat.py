from pydantic import BaseModel
from datetime import date
from user import UserModel
from message import MessageModel

class ChatModel(BaseModel):
    id: int
    created_at: date
    user: list[UserModel]
    messages = list[MessageModel]