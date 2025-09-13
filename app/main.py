from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict

from app.core.env import env
from app.core.database import db

# db 연결 확인
db = db

app = FastAPI(
    openapi_url=None if env.MODE == "prod" else "/openapi.json",
    docs_url=None if env.MODE == "prod" else "/docs",
    redoc_url=None if env.MODE == "prod" else "/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}
