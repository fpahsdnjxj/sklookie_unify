from fastapi import Depends, HTTPException
from db.repository import ChatRepository, UserRepository
from db.orm import Chat
from security import get_access_token
from service.users import UserService


class ChatService:
    def __init__(self, user_service: UserService, user_repo: UserRepository, chat_repo: ChatRepository):
        self.user_service = user_service
        self.user_repo = user_repo
        self.chat_repo = chat_repo

    def validate_chat_access(
            self, 
            chat_id: str, 
            access_token=Depends(get_access_token),
        ) -> Chat:
        user=self.user_service.authorize_user(access_token=access_token, user_repo=self.user_repo)
        chat = self.chat_repo.get_chat_by_chat_id(chat_id=chat_id)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat Not Found")
        if chat.user_id != user.user_id:
            raise HTTPException(status_code=403, detail="Permission Denied")
        return chat