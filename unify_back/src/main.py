from fastapi import FastAPI
from api import auth, message,chat, user, temp
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
app.include_router(message.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(user.router)
app.include_router(temp.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

