from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException

from db.orm import Users
from db.repository import UserRepository
from service.users import UserService

def get_access_token(
        auth_header:HTTPAuthorizationCredentials|None =Depends(HTTPBearer(auto_error=False)),
)->str:
    if auth_header is None:
        raise HTTPException(
            status_code=401,
            detail="Not Authorized",
        )
    return auth_header.credentials

