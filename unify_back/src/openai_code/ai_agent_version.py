from typing import List
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from prompts import system_message_prompt
import os

from schema.response import UserInfoResponse
from db.orm import Message

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/2023_pdf"))
db_2023 = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0
)

@tool
def search_yoram_2023(search_word):
    """Retrieve information from 2023 sogang university Catalog return context from catalog"""
    retrieved_docs = db_2023.similarity_search(search_word)
    return {"context": retrieved_docs}

def stringify_user_info(user: UserInfoResponse) -> str:
    return ", ".join([f"{key}: {value}" for key, value in user.model_dump().items() if value is not None])

def messages_to_string(messages: List[Message]) -> str:
    return "\n".join([f"Role: {message.message_role}, Content: {message.message_content}" for message in messages])

def get_answer_from_agent(question, userInfo, previousMessage):
    userInfo_string=stringify_user_info(userInfo)
    previousMessage_string=messages_to_string(previousMessage)
    prompt=system_message_prompt.invoke({"user_info":userInfo_string, "previous_message": previousMessage_string})
    tools=[search_yoram_2023]
    llm_with_tools=llm.bind_tools(tools)
    agent_executor=create_react_agent(llm_with_tools, tools, state_modifier=prompt)
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=question)]}
    ):
        pass
    final_message=chunk
    return final_message["agent"]["messages"][0].content

"""answer=get_answer_from_agent("경영학과 1학년 학생이 들어야 하는 과목을 추천해줘")
print(answer)"""
