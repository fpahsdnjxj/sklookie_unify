from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain import hub
from langchain_openai import ChatOpenAI

embeddings = OpenAIEmbeddings( model="text-embedding-3-large",)
db_2023 = FAISS.load_local('./db/2023_pdf', embeddings, allow_dangerous_deserialization=True)

prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0.7
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

response = graph.invoke({"question": "경제학과의 이론경제학 Honors Program에는 어떤 과목이 있는지 알려줘."})
print(response["answer"])