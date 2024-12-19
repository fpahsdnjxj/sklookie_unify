from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from db.connection import get_db
from db.repository import MessageRepository, get_message_by_chatid
from db.orm import Message
from schema.request import InputQuestion
from schema.response import MessageChatResponse
from openai_code.chat_answer import graph

router=APIRouter(prefix="/chat")

@router.post("/", status_code=201)
async def answer(
    #chat_id:str,
    data: InputQuestion,
    message_repo: MessageRepository=Depends()
    ):
    user_input = data.question
    print(f"Received question: {user_input}")
    if user_input.strip():
        response = graph.invoke({"question": user_input})
        return {"answer": response["answer"]}
    raise HTTPException(status_code=404, detail="question not found")


@router.get("/{chat_id}", status_code=200)
async def look_messages(
    chat_id: str,
    message_repo: MessageRepository=Depends(),
    ):
    message_list: List[Message]=message_repo.get_message_by_chatid(chat_id)
    if message_list:
        return message_list
    else:
        raise HTTPException(status_code=404, detail="Message not found")

