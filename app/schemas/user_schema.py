from pydantic import BaseModel, Field

from app.core.enums import STORE_SPOT


class LoginRequest(BaseModel):
    user_id: str = Field(..., description="사용자 아이디")
    password: str = Field(..., description="비밀번호")
    store_spot: STORE_SPOT = Field(..., description="지점")


class Token(BaseModel):
    access_token: str = Field(..., description="액세스 토큰")
    token_type: str = Field(..., description="토큰 타입")


class TokenData(BaseModel):
    user_id: str | None = None
