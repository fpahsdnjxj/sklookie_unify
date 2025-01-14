from typing import List
from fastapi import APIRouter, Depends, HTTPException
from db.orm import Chat, Users
from db.repository import ChatRepository, UserRepository
from schema.request import CreateChatRequest, UpdateChatnameRequest
from schema.response import ChatSchema, ListChatResponse
from security import get_access_token
from service.users import UserService
from service.chat import ChatService



router=APIRouter(prefix="/api/chat")

def get_chat_service(
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends(),
    chat_repo: ChatRepository = Depends(),
) -> ChatService:
    return ChatService(user_service=user_service, user_repo=user_repo, chat_repo=chat_repo)

@router.get("", status_code=200)
def get_chats_handler(
    access_token=Depends(get_access_token),
    user_service:UserService=Depends(),
    user_repo:UserRepository=Depends()
)->ListChatResponse:
    user=user_service.authorize_user(access_token=access_token, user_repo=user_repo)
    chats:List[Chat]=user.chats
    return ListChatResponse(chats=[ChatSchema(chat_id=chat.chat_id,chat_name=chat.chat_name, start_date=chat.start_date) for chat in chats])

@router.post("", status_code=201)
def create_chat_handler(
    request: CreateChatRequest,
    access_token=Depends(get_access_token),
    user_service:UserService=Depends(),
    user_repo:UserRepository=Depends(),
    chat_repo:ChatRepository=Depends()
)->ChatSchema:
    user=user_service.authorize_user(access_token=access_token, user_repo=user_repo)
    chat:Chat=Chat.create(user_id=user.user_id, chat_name=request.chat_name)
    chat:Chat=chat_repo.create_chat(chat=chat)
    return ChatSchema.model_validate(chat)


@router.patch("/{chat_id}", status_code=200)
def update_chat_handler(
    chat_id: str,
    request: UpdateChatnameRequest,
    access_token: str = Depends(get_access_token),
    chat_service: ChatService = Depends(get_chat_service),
):
    chat = chat_service.validate_chat_access(chat_id=chat_id, access_token=access_token)
    chat.chat_name=request.chat_name
    chat=chat_service.chat_repo.update_chat(chat=chat)
    return ChatSchema.model_validate(chat)


@router.delete("/{chat_id}", status_code=204)
def delete_chat(
    chat_id: str,
    access_token: str = Depends(get_access_token),
    chat_service: ChatService = Depends(get_chat_service),
):
    chat = chat_service.validate_chat_access(chat_id=chat_id, access_token=access_token)
    chat_service.chat_repo.delete_chat(chat.chat_id)
