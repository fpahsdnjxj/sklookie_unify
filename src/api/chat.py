from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.orm import Chat, Users
from db.repository import ChatRepository, UserRepository
from schema.request import CreateChatRequest
from schema.response import ChatSchema, ListChatResponse
from security import get_access_token
from service.users import UserService


router=APIRouter(prefix="/chat")

@router.get("", status_code=200)
def get_chats_handler(
    access_token=Depends(get_access_token),
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
)->ListChatResponse:
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    chats:List[Chat]=user.chats
    return ListChatResponse(chats=[ChatSchema(chat_name=chat.chat_name, start_date=chat.start_date) for chat in chats])

@router.post("", status_code=201)
def create_chat_handler(
    request: CreateChatRequest,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
    chat_repo: ChatRepository=Depends()
)->ChatSchema:
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    chat:Chat=Chat.create(user_id=user.user_id, chat_name=request.chat_name)
    chat:Chat=chat_repo.create_chat(chat=chat)
    return ChatSchema.model_validate(chat)

