from fastapi import FastAPI
from api import chat

app=FastAPI()
app.include_router(chat.router)

@app.get("/", status_code=200)
async def signin():
    return "HI"

