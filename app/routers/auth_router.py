from fastapi import APIRouter

from app.schemas.user_schema import Token, LoginRequest
from app.services.auth_service import AuthService
from app.core.enums import STORE_SPOT  # STORE_SPOT 임포트


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    token = await AuthService.login_for_access_token(login_request)
    return token


@router.get("/store-spots", response_model=list[STORE_SPOT])  # 새로운 엔드포인트
async def get_store_spots():
    return list(STORE_SPOT)
