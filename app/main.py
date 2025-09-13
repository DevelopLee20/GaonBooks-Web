from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Any, Dict
from contextlib import asynccontextmanager

from app.core.env import env
from app.collections import create_all_indexes
from app.routers import book_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On application startup
    await create_all_indexes()
    yield
    # On application shutdown
    pass


app = FastAPI(
    openapi_url=None if env.MODE == "prod" else "/openapi.json",
    docs_url=None if env.MODE == "prod" else "/docs",
    redoc_url=None if env.MODE == "prod" else "/redoc",
    lifespan=lifespan,
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/assets/favicon.ico")


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}
