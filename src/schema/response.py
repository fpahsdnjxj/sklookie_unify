from datetime import datetime
from typing import List
from pydantic import BaseModel
from enum import Enum


class UserSchema(BaseModel):
    user_loginid: str
    user_name: str

    class Config:
        from_attributes=True

class ListUserResponse(BaseModel):
    users: List[UserSchema]

class ChatSchema(BaseModel):
    chat_name: str
    start_date: datetime

    class Config:
        from_attributes=True

class ListChatResponse(BaseModel):
    chats: List[ChatSchema]

class RoleEnum(str, Enum):
    USER="user"
    AI="ai"
    ADMIN="admin"

class MessageSchema(BaseModel):
    message_date: datetime
    message_role: RoleEnum
    message_content:str

    class Config:
        from_attributes=True

class MessageChatResponse(BaseModel):
    messages: List[MessageSchema]

class JWTResponse(BaseModel):
    access_token:str

