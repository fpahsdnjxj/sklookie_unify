from fastapi import APIRouter, Depends, HTTPException
from db.orm import Users
from db.repository import UserRepository
from schema.request import LogInRequest, SignUpRequest, UpdateUserinfoRequest
from schema.response import JWTResponse, UserInfoResponse, UserSchema
from security import get_access_token
from service.users import UserService


router=APIRouter(prefix="/user")

#유저 정보 수집
@router.get("", status_code=200)
def user_login_handler(
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    
    return UserInfoResponse.model_validate(user)


## 유저 정보 수정
@router.patch("/update", status_code=200)
def user_login_handler(
    request: UpdateUserinfoRequest,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    user.user_name= request.user_name
    user.user_major=request.user_major
    user.user_semester=request.user_semester
    user.user_info=request.user_info
    user=user_repo.update_user(user=user)
    return UserInfoResponse.model_validate(user)

##회원 탈퇴(chat이랑 message도 다 지워지도록 변경 필요)
@router.delete("/{user_loginid}", status_code=204)
def user_login_handler(
    user_loginid:str,
    user_service: UserService=Depends(),
    user_repo:UserRepository=Depends(),
    access_token=Depends(get_access_token),
):
    user_loginid:str=user_service.decode_jwt(access_token=access_token)
    user: Users|None=user_repo.get_user_by_loginid(user_loginid=user_loginid)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    user_repo.delete_user(user_loginid=user.user_loginid)
    

