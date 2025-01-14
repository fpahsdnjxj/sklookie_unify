from fastapi import APIRouter, Depends, HTTPException
from db.orm import Users
from db.repository import UserRepository
from schema.request import UpdateUserinfoRequest
from schema.response import UserInfoResponse
from security import get_access_token
from service.users import UserService

router=APIRouter(prefix="/api/user")

#유저 정보 수집
@router.get("", status_code=200)
def user_get_info(
    access_token=Depends(get_access_token),
    user_service:UserService=Depends(),
    user_repo:UserRepository=Depends()
):    
    user=user_service.authorize_user(access_token=access_token, user_repo=user_repo)
    return UserInfoResponse.model_validate(user)


## 유저 정보 수정
@router.patch("/update", status_code=200)
def user_update_info(
    request: UpdateUserinfoRequest,
    access_token=Depends(get_access_token),
    user_service:UserService=Depends(),
    user_repo:UserRepository=Depends()
):
    user=user_service.authorize_user(access_token=access_token, user_repo=user_repo)
    user.user_name= request.user_name
    user.user_major=request.user_major
    user.user_semester=request.user_semester
    user.user_info=request.user_info
    user=user_repo.update_user(user=user)
    return UserInfoResponse.model_validate(user)

##회원 탈퇴(chat이랑 message도 다 지워지도록 변경 필요)
@router.delete("/delete", status_code=204)
def user_delete(
    access_token=Depends(get_access_token),
    user_service:UserService=Depends(),
    user_repo:UserRepository=Depends()
):
    user=user_service.authorize_user(access_token=access_token, user_repo=user_repo)
    user_repo.delete_user(user_id=user.user_id)


    

