from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handler import router
import asyncio
import logging
import config
import os


bot = Bot(token=os.environ.get("BOT_TOKEN"))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    asyncio.run(main())
