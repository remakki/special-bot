import asyncio

from src.bot import start_bot


async def main():
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
