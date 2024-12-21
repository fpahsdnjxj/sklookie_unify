from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.connection import get_db
from db.orm import Users, Chat, Message

class UserRepository:
    def __init__(self, session:Session=Depends(get_db)):
        self.session=session

    def get_users(self)->List[Users]:
        return list(self.session.scalars(select(Users)))

    def save_user(self, users: Users)->Users:
        self.session.add(instance=users)
        self.session.commit()
        self.session.refresh(instance=users)
        return users
    
    def get_user_by_loginid(self, user_loginid:str)->Users|None:
        return self.session.scalar(select(Users).where(Users.user_loginid==user_loginid))
class ChatRepository:
    def __init__(self, session:Session=Depends(get_db)):
        self.session=session

    def get_chat_by_userid(self, user_id: str)->List[Chat]|None:
        return list(self.session.scalars(select(Chat).where(Chat.user_id==user_id)))
    
    def create_chat(self, chat: Chat)->Chat:
        self.session.add(instance=chat)
        self.session.commit()
        self.session.refresh(instance=chat)
        return chat

class MessageRepository:
    def __init__(self, session:Session=Depends(get_db)):
        self.session=session

    def get_message_by_chatid(self, chat_id: str)->List[Message]|None:
        return list(self.session.scalars(select(Message).where(Message.chat_id==chat_id)))