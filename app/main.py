from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
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


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"I'm ready": "OK"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5555)
