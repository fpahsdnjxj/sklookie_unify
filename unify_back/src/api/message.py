from typing import List
from fastapi import Depends, APIRouter, WebSocket, WebSocketException, status
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketDisconnect

from db.repository import MessageRepository
from db.orm import Chat, Message, Users
from schema.response import UserInfoResponse
from schema.request import TestMessageRequest
from api.chat import get_chat_service
from security import get_access_token
from service.chat import ChatService
from openai_code.ai_agent_version import get_answer_from_agent


router=APIRouter(prefix="/api/message")

## 차후에 도입해볼 websocket
@router.websocket("/{chat_id}")
async def chat_wesocket_handler(
    chat_id:str,
    websocket: WebSocket,
    access_token: str = Depends(get_access_token),
    chat_service: ChatService = Depends(get_chat_service),
    ):
    chat = chat_service.validate_chat_access(chat_id=chat_id, access_token=access_token)
    chat:Chat=chat_service.chat_repo.get_chat_by_chat_id(chat_id=chat_id)
    if not chat:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    await websocket.accept()
    try:
        while True:
            user_input=await websocket.receive_text()
            if user_input.strip():
                response = get_answer_from_agent(user_input)
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
    access_token: str = Depends(get_access_token),
    chat_service: ChatService = Depends(get_chat_service),
    ):
    chat_service.validate_chat_access(chat_id=chat_id, access_token=access_token)
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    return message_list or []

@router.post("/{chat_id}",status_code=201)
async def test_message(
    chat_id:str,
    request:TestMessageRequest,
    message_repo: MessageRepository=Depends(),
    access_token: str = Depends(get_access_token),
    chat_service: ChatService = Depends(get_chat_service),
):
    chat:Chat=chat_service.validate_chat_access(chat_id=chat_id, access_token=access_token)
    user: Users = chat_service.user_service.authorize_user(access_token=access_token, user_repo=chat_service.user_repo)
    
    #데이터 가져옴
    user_info=UserInfoResponse.model_validate(user)
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    next_message_id = len(message_list) + 1

    #질문 저장
    user_message:Message=Message.create(message_id=next_message_id, chat_id=chat.chat_id, message_content=request.question, message_role="user")
    message_repo.create_message(message=user_message)

    #답변생성
    response = get_answer_from_agent(request.question, user_info, message_list)
    
    #답변저장
    ai_message:Message=Message.create(message_id=next_message_id+1, chat_id=chat.chat_id, message_content=response, message_role="ai")
    message_repo.create_message(message=ai_message)
    return JSONResponse(content={"data": ai_message.message_content})