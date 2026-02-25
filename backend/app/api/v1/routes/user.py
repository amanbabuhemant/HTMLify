from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.models import User
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from ..schemas.user import *


router = APIRouter()


@router.get("/users/me")
def get_my_info(user: User = Depends(AuthService.get_current_user)) -> UserFullInfo:
    return UserFullInfo.from_orm(user)

@router.get("/users/{username}")
def get_user_info(username: str) -> UserPublicInfo:
    user = UserService.get_user(username)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "User not found with this username"
        )
    return UserPublicInfo.from_orm(user)

@router.get("/users/me/api-key")
def get_my_api_key(user: User = Depends(AuthService.get_current_user)) -> APIKeyResponse:
    return APIKeyResponse(api_key=str(user.api_key))

