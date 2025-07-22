from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from loguru import logger


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🏁 Start bot / Show help"),
        BotCommand(command="set_ocr", description="⚙️ Set OCR engine"),
        BotCommand(command="my_ocr", description="👀 Show current OCR engine"),
        BotCommand(command="set_lang", description="🗣️ Set OCR language"),
        BotCommand(command="my_lang", description="🌍 Show current OCR language"),
        BotCommand(command="limits", description="📊 Show usage limits"),
    ]
    try:
        await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
        logger.info("Bot commands have been successfully installed/updated.")
    except Exception as e:
        logger.error(f"Error when installing bot commands: {e}")
