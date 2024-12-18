from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain import hub
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

# 시스템 메시지 템플릿 생성
system_message_prompt = SystemMessagePromptTemplate.from_template("""
System: You are an AI designed to provide information using university catalog data and course offerings. 
Please follow these guidelines:
1. Provide clear and specific answers to user questions.
2. If the requested data cannot be found, respond with: "The relevant data cannot be found. Please ask a more specific question."
3. Deliver logical and intuitive responses. Avoid illogical answers and request clarification if the question is unclear.
4. Match key data points (e.g., department name, credits, course name) precisely to the user's query.
5. After providing the requested information, encourage follow-up questions to enhance the user experience.

Question: {question} 

Context: {context} 
Answer:
""")

# 사용자 메시지 템플릿 생성
human_message_prompt = HumanMessagePromptTemplate.from_template("""
You are an assistant for question-answering tasks. Use the following pieces of retrieved 
context to answer the question. If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
""")

# ChatPromptTemplate 생성
prompt = ChatPromptTemplate.from_messages([
    system_message_prompt,
    human_message_prompt
])


embeddings = OpenAIEmbeddings( model="text-embedding-3-large",)
db_2023 = FAISS.load_local('./db/2023_pdf', embeddings, allow_dangerous_deserialization=True)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.0
)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = db_2023.similarity_search(state["question"])
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

def main():
    st.title("유니피")
    st.write("안녕하세요 저는 유니피에요. 원하는 질문을 입력해주세요.")
    user_input = st.text_input("질문을 입력하세요")
    if st.button("Send"):
        response = graph.invoke({"question": user_input})
        st.write(response["answer"])
        

if __name__ == "__main__":
    main()

