from fastapi import APIRouter, Depends, HTTPException
from db.orm import Users
from db.repository import UserRepository
from schema.request import UpdateUserinfoRequest
from schema.response import UserInfoResponse
from security import user_authorization



router=APIRouter(prefix="/user")

#유저 정보 수집
@router.get("", status_code=200)
def user_get_info(
    user:Users=Depends(user_authorization)
):    
    return UserInfoResponse.model_validate(user)


## 유저 정보 수정
@router.patch("/update", status_code=200)
def user_update_info(
    request: UpdateUserinfoRequest,
    user:Users=Depends(user_authorization),
    user_repo:UserRepository=Depends(),
):
    user.user_name= request.user_name
    user.user_major=request.user_major
    user.user_semester=request.user_semester
    user.user_info=request.user_info
    user=user_repo.update_user(user=user)
    return UserInfoResponse.model_validate(user)

##회원 탈퇴(chat이랑 message도 다 지워지도록 변경 필요)
@router.delete("/delete", status_code=204)
def user_delete(
    user_repo:UserRepository=Depends(),
    user:Users=Depends(user_authorization),
):
    user_repo.delete_user(user_id=user.user_id)


    

