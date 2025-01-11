from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
import os

from openai_code.prompts import prompt, search_prompt
from schema.response import UserInfoResponse
from db.orm import Message

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/2023_pdf"))
db_2023 = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0
)

class State(TypedDict):
    user_info: UserInfoResponse
    question: str
    context: List[Document]
    previous_message: List[Message]
    search_word:str
    answer: str

def stringify_user_info(user: UserInfoResponse) -> str:
    return ", ".join([f"{key}: {value}" for key, value in user.model_dump().items() if value is not None])

def messages_to_string(messages: List[Message]) -> str:
    return "\n".join([f"Role: {message.message_role}, Content: {message.message_content}" for message in messages])

def redefine_question(state:State):
    if not state["question"] or not isinstance(state["question"], str):
        raise ValueError("The question must be a non-empty string.")
    user_info_string=stringify_user_info(state["user_info"])
    message=search_prompt.invoke({"user_info":user_info_string, "question":state["question"]})
    response=llm.invoke(message)
    state["search_word"]=response.content
    print(state['search_word'])

def retrieve(state: State):
    redefine_question(state)
    if not state["search_word"] or not isinstance(state["search_word"], str):
        raise ValueError("The question must be a non-empty string.")
    retrieved_docs = db_2023.similarity_search(state["search_word"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    user_info_string=stringify_user_info(state["user_info"])
    messages_list=messages_to_string(state["previous_message"])
    messages = prompt.invoke({"user_info":user_info_string, "question": state["question"], "context": docs_content, "previous_message": messages_list})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State)
graph_builder.add_edge(START, "retrieve")
graph_builder.add_sequence([retrieve, generate])
graph = graph_builder.compile()


