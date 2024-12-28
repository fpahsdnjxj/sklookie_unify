from typing import Optional
from pydantic import BaseModel


class SignUpRequest(BaseModel):
        user_loginid:str
        user_password:str
        user_name:str

class LogInRequest(BaseModel):
        user_loginid:str
        user_password:str

class CreateChatRequest(BaseModel):
        chat_name:str

class UpdateChatnameRequest(BaseModel):
        chat_name:str

class UpdateUserinfoRequest(BaseModel):
    user_name:Optional[str]=None
    user_semester:Optional[int]=None
    user_major:Optional[str]=None
    user_info:Optional[str]=None
