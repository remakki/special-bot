from aiogram import BaseMiddleware
from aiogram.types import Update
from redis.asyncio import Redis


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis):
        super().__init__()
        self.redis = redis

    async def __call__(self, handler, event: Update, data: dict):
        data["redis"] = self.redis
        return await handler(event, data)


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(self, handler, event: Update, data: dict):
        if hasattr(event, "message") and event.message:
            username = event.message.from_user.username
            redis = data["redis"]

            admins = [
                admin.decode("utf-8") for admin in await redis.lrange("admins", 0, -1)
            ]
            data["is_admin"] = username in admins

        return await handler(event, data)
