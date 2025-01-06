from fastapi import APIRouter, Depends, HTTPException
from db.orm import Users
from db.repository import UserRepository
from schema.request import LogInRequest, SignUpRequest
from schema.response import JWTResponse, UserSchema
from service.users import UserService


router=APIRouter(prefix="/auth")

@router.post("/sign-up", status_code=201)
def user_sign_up_handler(
    request: SignUpRequest,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
):
    hashed_password:str=user_service.hash_password(plain_password=request.user_password)
    users:Users=Users.create(user_name=request.user_name, user_loginid=request.user_loginid, user_password=hashed_password)
    users:Users=user_repo.save_user(users=users)
    return UserSchema.model_validate(users)

@router.post("/login")
def user_login_handler(
    request:LogInRequest,
    user_repo:UserRepository=Depends(),
    user_service: UserService=Depends(),
):
    users:Users|None=user_repo.get_user_by_loginid(user_loginid=request.user_loginid)
    if not users:
        raise HTTPException(status=404, detail="User not found")
    
    verified:bool=user_service.verify_password(plain_password=request.user_password, hashed_password=users.user_password)
    if not verified:
        raise HTTPException(status=401, detail="Not Authorized")
    
    access_token:str=user_service.create_jwt(user_loginid=users.user_loginid)
    return JWTResponse(access_token=access_token)

