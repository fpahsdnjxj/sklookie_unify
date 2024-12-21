from sqlalchemy import Column, Integer, String, Text, CHAR, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import uuid
from datetime import datetime, timezone

Base=declarative_base()

class Users(Base):
    __tablename__="Users"

    user_id=Column(CHAR(36), primary_key=True, index=True, default=lambda:(uuid.uuid4()))
    user_loginid=Column(String(50), nullable=False, unique=True)
    user_password=Column(String(255), nullable=False)
    user_name=Column(String(50), nullable=False)
    user_semester=Column(Integer)
    user_major=Column(String(50))
    user_info=Column(Text)

    chats=relationship("Chat", lazy="joined")

    def __repr__(self):
        return f"Users(login_id={self.user_loginid}, password={self.user_password}, name={self.user_name})"
    
    @classmethod
    def create(cls, user_loginid:str, user_password:str, user_name:str)->"Users":
        return cls(
                user_loginid= user_loginid,
                user_password=user_password,
                user_name=user_name,
        )


class Chat(Base):
    __tablename__="Chat"
    
    chat_id=Column(CHAR(36), primary_key=True, default=lambda:(uuid.uuid4()))
    user_id=Column(CHAR(36), ForeignKey("Users.user_id"), primary_key=True)
    start_date=Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    chat_name=Column(String(50), nullable=False)

    def __repr__(self):
        return f"Chat(chat_id={self.chat_id}, user_id={self.user_id}, chat_name={self.chat_name}, start_date={self.start_date})"
    
    @classmethod
    def create(cls, user_id:str, chat_name:str)->"Users":
        return cls(
            user_id=user_id,
            chat_name=chat_name,
        )
    
    


class Message(Base):
    __tablename__="Message"

    message_id=Column(Integer, primary_key=True, index=True)
    chat_id=Column(CHAR(36), ForeignKey("Chat.chat_id"), primary_key=True)
    message_time=Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    message_content=Column(Text, nullable=False)
    message_role = Column(Enum("user", "ai", "admin", name="message_roles"), nullable=False)

    def __repr__(self):
        return (
            f"Message("
            f"message_id={self.message_id}, "
            f"chat_id={self.chat_id}, "
            f"message_time={self.message_time}, "
            f"message_content='{self.message_content[:30]}...', "  # 내용이 길 경우 앞 30자만 표시
            f"message_role={self.message_role})"
        )