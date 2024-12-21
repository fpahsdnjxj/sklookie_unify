import bcrypt
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os


class UserService:
    encoding: str="UTF-8"
    secret_key:str=os.getenv("SECRET_KEY")
    jwt_algorithm: str="HS256"

    def hash_password(self, plain_password:str)->str:
        hashed_password: bytes=bcrypt.hashpw(plain_password.encode(self.encoding), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encoding)
    
    def verify_password(self, plain_password:str, hashed_password: str)->bool:
        return bcrypt.checkpw(plain_password.encode(self.encoding), hashed_password.encode(self.encoding))
    
    def create_jwt(self, user_loginid:str)->str:
        return jwt.encode(
            {
             "sub":user_loginid, 
             "exp":datetime.now()+timedelta(days=1)
             }, 
            self.secret_key, 
            algorithm=self.jwt_algorithm,
        )
    
    def decode_jwt(self, access_token:str):
        payload:dict=jwt.decode(
            access_token,self.secret_key, algorithms=[self.jwt_algorithm]
        )
        return payload["sub"]
    