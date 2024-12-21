from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.orm import Chat, Users
from db.repository import ChatRepository, UserRepository
from schema.request import CreateChatRequest, UpdateChatnameRequest
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
    return ListChatResponse(chats=[ChatSchema(chat_id=chat.chat_id,chat_name=chat.chat_name, start_date=chat.start_date) for chat in chats])

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

@router.delete("/{chat_id}", status_code=204)
def update_chat_handler(
    chat_id:str,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
    chat_repo: ChatRepository=Depends()
):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat Not Found")
    if chat.user_id!=user.user_id:
        raise HTTPException(status_code=403, detail="Permission Denied")
    chat_repo.delete_chat(chat_id)

@router.patch("/{chat_id}", status_code=200)
def update_chat_handler(
    chat_id: str,
    request: UpdateChatnameRequest,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
    chat_repo: ChatRepository=Depends()
):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat Not Found")
    if chat.user_id!=user.user_id:
        raise HTTPException(status_code=403, detail="Permission Denied")
    chat.chat_name=request.chat_name
    chat=chat_repo.update_chat(chat=chat)
    return ChatSchema.model_validate(chat)

