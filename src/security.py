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

def user_authorization(
        access_token=Depends(get_access_token),
        user_service:UserService=Depends(),
        user_repo:UserRepository=Depends(),
    ):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user