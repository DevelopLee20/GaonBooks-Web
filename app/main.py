from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Any, Dict
from contextlib import asynccontextmanager
from bson import ObjectId  # Import ObjectId

from app.core.env import env
from app.collections import create_all_indexes
from app.routers import book_router, auth_router
from app.core.security import get_current_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 초기 DB 인덱스 설정
    await create_all_indexes()

    yield
    # On application shutdown
    pass


app = FastAPI(
    openapi_url=None if env.MODE == "prod" else "/openapi.json",
    docs_url=None if env.MODE == "prod" else "/docs",
    redoc_url=None if env.MODE == "prod" else "/redoc",
    lifespan=lifespan,
    json_encoders={ObjectId: str},  # Add this line
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the book router
app.include_router(book_router.router)
app.include_router(auth_router.router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/assets/favicon.ico")


@app.get("/", dependencies=[Depends(get_current_user)])
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}
