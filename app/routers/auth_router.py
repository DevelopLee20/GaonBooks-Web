from fastapi import APIRouter

from app.schemas.user_schema import Token, LoginRequest
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    token = await AuthService.login_for_access_token(login_request)
    return token
