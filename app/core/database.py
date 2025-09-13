from motor.motor_asyncio import AsyncIOMotorClient

from app.core.env import env

# 비동기 클라이언트
client = AsyncIOMotorClient(env.DB_URI)

db = client["base"]
