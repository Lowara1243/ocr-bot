import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger
from utils.bot_commands import set_bot_commands

import config
from database.db import Database
from handlers.user_handlers import register_user_handlers


async def on_startup(bot: Bot):
    await Database.init_db()
    await set_bot_commands(bot)
    logger.info("Bot started and commands are set.")

async def on_shutdown():
    logger.info("Bot shutting down...")
    await Database.close_connection()
    logger.info("Database connection closed. Shutdown complete.")

async def main():
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)
    )
    dp = Dispatcher()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    register_user_handlers(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user.")
