from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.orm import Users, Chat, Message

def get_users(session: Session)->List[Users]:
    return list(session.scalars(select(Users)))

def get_chat(session: Session)->List[Chat]:
    return list(session.scalars(select(Chat)))

def get_message(session: Session)->List[Message]:
    return list(session.scalars(select(Message)))