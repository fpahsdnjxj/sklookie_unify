import json
from typing import List
from fastapi import HTTPException, Depends, APIRouter, WebSocket, WebSocketException, status
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session

from db.connection import get_db
from db.repository import ChatRepository, MessageRepository, UserRepository
from db.orm import Chat, Message, Users
from schema.response import MessageChatResponse, UserInfoResponse
from openai_code.chat_answer import graph
from security import user_authorization
from schema.request import TestMessageRequest


router=APIRouter(prefix="/message")


@router.websocket("/{chat_id}")
async def chat_wesocket_handler(
    chat_id:str,
    websocket: WebSocket,
    user:Users=Depends(user_authorization),
    chat_repo: ChatRepository=Depends(),
    ):
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
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
    user:Users=Depends(user_authorization),
    chat_repo: ChatRepository=Depends(),
    ):
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id!=user.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    return message_list or []

@router.post("/{chat_id}",status_code=201)
async def test_message(
    chat_id:str,
    request:TestMessageRequest,
    message_repo: MessageRepository=Depends(),
    user:Users=Depends(user_authorization),
    chat_repo: ChatRepository=Depends(),
):
    chat:Chat=chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.user_id!=user.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access")
    
    #데이터 가져옴
    user_info=UserInfoResponse.model_validate(user)
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    next_message_id = len(message_list) + 1

    #질문 저장
    user_message:Message=Message.create(message_id=next_message_id, chat_id=chat.chat_id, message_content=request.question, message_role="user")
    message_repo.create_message(message=user_message)

    #답변생성
    response = graph.invoke({ "user_info": user_info, "question": request.question, "previous_message": message_list})
    
    #답변저장
    ai_message:Message=Message.create(message_id=next_message_id+1, chat_id=chat.chat_id, message_content=response["answer"], message_role="ai")
    message_repo.create_message(message=ai_message)
    return JSONResponse(content={"data": ai_message.message_content})