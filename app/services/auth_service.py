from datetime import timedelta

from fastapi import HTTPException, status

from app.collections.user_collection import UserCollection
from app.core import security
from app.core.env import env
from app.schemas.user_schema import LoginRequest, Token


class AuthService:
    @classmethod
    async def login_for_access_token(cls, login_request: LoginRequest) -> Token:
        user = await UserCollection.get_user_by_user_id(login_request.user_id)

        if (
            not user
            or not security.verify_password(
                login_request.password, user.hashed_password
            )
            or user.store_spot != login_request.store_spot
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="로그인 정보가 올바르지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            data={"sub": user.user_id}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
