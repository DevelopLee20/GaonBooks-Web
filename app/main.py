from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Any, Dict

from app.core.env import env

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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("assets/favicon.ico")


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}
