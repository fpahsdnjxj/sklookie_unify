from pydantic import BaseModel

class InputQuestion(BaseModel):
        question: str

class SignUpRequest(BaseModel):
        user_loginid:str
        user_password:str
        user_name:str

class LogInRequest(BaseModel):
        user_loginid:str
        user_password:str

class CreateChatRequest(BaseModel):
        chat_name:str