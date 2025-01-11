import time
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2024-05-01-preview",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

system_prompt="""
You are an AI specialized in providing information based on university catalog data and course offerings. Follow these guidelines:

1. Deliver clear, specific, and accurate answers to user questions.
2. If the requested data is unavailable, respond with: "관련 정보는 요람에서 찾을 수 없습니다."
3. Provide logical, intuitive responses. If a question is unclear, politely ask for clarification.
4. Ensure key data points (e.g., department name, credits, course name) match the user’s query precisely.
5. After answering, invite follow-up questions to improve the user experience.
"""
assistant = client.beta.assistants.create(
  name="University course Assistant",
  instructions=system_prompt,
  model="gpt-4o-mini",
  tools=[{"type": "file_search"}],
)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": os.getenv("2023_FILE_ID")}},
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="경영통계학이 뭐하는 수업인지 알려줘줘"
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    time.sleep(1)

messages = client.beta.threads.messages.list(thread_id=thread.id)
for message in messages:
    if message.role == "assistant":
        print(message.content[0].text.value)