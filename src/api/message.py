from typing import List
from fastapi import HTTPException, Depends, APIRouter, WebSocket, WebSocketException, status
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session

from db.connection import get_db
from db.repository import ChatRepository, MessageRepository, UserRepository
from db.orm import Chat, Message, Users
from schema.response import MessageChatResponse
from openai_code.chat_answer import graph
from security import get_access_token
from service.users import UserService

router=APIRouter(prefix="/message")


@router.websocket("/{chat_id}")
async def chat_wesocket_handler(
    chat_id:str,
    websocket: WebSocket,
    access_token=Depends(get_access_token),
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    chat_repo: ChatRepository=Depends(),
    ):
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if user.user_id!=chat.user_id:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    await websocket.accept()
    try:
        while True:
            user_input=await websocket.receive_text()
            if user_input.strip():
                response = graph.invoke({"question": user_input})
            await websocket.send_text(response["answer"])
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for chat_id: {chat_id}")
    except Exception as e:
        print(f"Error in WebSocket: {e}")
        await websocket.close(code=1001)



@router.get("/{chat_id}", status_code=200)
async def look_messages(
    chat_id: str,
    message_repo: MessageRepository=Depends(),
    access_token=Depends(get_access_token),
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    chat_repo: ChatRepository=Depends(),
    ):
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if user.user_id!=chat.user_id:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    return message_list or []

