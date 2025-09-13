from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from src.bot.handlers import register_handlers
from src.bot.middleware import RedisMiddleware, AuthMiddleware
from src.config import settings

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def start_bot():
    async with Redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}"
    ) as redis:
        storage = RedisStorage(redis)
        dp = Dispatcher(storage=storage)

        await redis.rpush("admins", settings.ADMIN_TELEGRAM_USERNAME)
        dp.update.middleware(RedisMiddleware(redis))
        dp.update.middleware(AuthMiddleware())

        register_handlers(dp)

        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()
