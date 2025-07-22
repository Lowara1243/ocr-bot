import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, PhotoSize
from loguru import logger

from .. import config
from ..config import ADMIN_ID
from ..database.db import Database
from ..ocr_engines import get_ocr_engine, ENGINES
from ..utils.rate_limiter import RateLimiter

user_router = Router()


def escape_markdown_v2(text: str) -> str:
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


@user_router.message.middleware()
async def user_setup_middleware(handler, event: Message, data: dict):
    await Database.add_or_update_user(
        user_id=event.from_user.id,
        username=event.from_user.username,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
    )
    return await handler(event, data)


@user_router.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f"User {message.from_user.id} started bot.")

    available_engines_str = ", ".join([escape_markdown_v2(e) for e in ENGINES.keys()])
    supported_langs_str = ", ".join(
        [escape_markdown_v2(lang) for lang in config.SUPPORTED_OCR_LANGUAGES]
    )

    text = (
        "Hello\\! I'm an OCR bot\\. Send me an image, and I'll transcribe the text\\.\n\n"
        "Available commands:\n"
        "/set\\_ocr `<engine>` \\- Change OCR engine \\(e\\.g\\., `/set_ocr tesseract`\\)\\.\n"
        f"Available: `{available_engines_str}`\n\n"
        "/my\\_ocr \\- Show your current OCR engine\\.\n\n"
        "/set\\_lang `<lang_code>` \\- Set OCR language \\(e\\.g\\., `/set_lang rus`\\)\\.\n"
        f"Supported: `{supported_langs_str}`\n"
        "\\(For Tesseract, you can use `+`, e\\.g\\., `eng+rus`\\)\\.\n\n"
        "/my\\_lang \\- Show your current OCR language\\.\n\n"
        "/limits \\- Show your usage and limits\\."
    )
    await message.reply(text)


@user_router.message(Command("set_ocr"))
async def handle_set_ocr(message: Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)

    available_engines_str = ", ".join([escape_markdown_v2(e) for e in ENGINES.keys()])

    if len(args) < 2:
        await message.reply(
            f"Usage: `/set_ocr <engine_name>`\nAvailable: `{available_engines_str}`"
        )
        return

    engine_name = args[1].lower()
    if engine_name not in ENGINES:
        await message.reply(
            f"Invalid engine: `{escape_markdown_v2(engine_name)}`\\.\nAvailable: `{available_engines_str}`"
        )
        return

    await Database.set_user_ocr_preference(user_id, engine_name)
    logger.info(f"User {user_id} set OCR preference to {engine_name}")
    await message.reply(
        f"Your OCR engine is set to: *{escape_markdown_v2(engine_name)}*"
    )


@user_router.message(Command("my_ocr"))
async def handle_my_ocr(message: Message):
    preference = await Database.get_user_ocr_preference(message.from_user.id)
    await message.reply(
        f"Your current OCR engine is: *{escape_markdown_v2(preference)}*"
    )


@user_router.message(Command("set_lang"))
async def handle_set_lang(message: Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=1)
    supported_langs_str = ", ".join(
        [escape_markdown_v2(lang) for lang in config.SUPPORTED_OCR_LANGUAGES]
    )

    if len(args) < 2:
        await message.reply(
            f"Usage: `/set_lang <lang_code>`\nSupported: `{supported_langs_str}`"
        )
        return

    lang_code = args[1].lower()
    is_valid = all(
        part in config.SUPPORTED_OCR_LANGUAGES for part in lang_code.split("+")
    )

    if not is_valid:
        await message.reply(
            f"Invalid language code: `{escape_markdown_v2(lang_code)}`\\.\n"
            f"Supported codes: `{supported_langs_str}`\\.\n"
            f"Combine with `+` for Tesseract, e\\.g\\., `eng+rus`\\."
        )
        return

    await Database.set_user_ocr_language(user_id, lang_code)
    logger.info(f"User {user_id} set OCR language to {lang_code}")
    await message.reply(
        f"Your OCR language is set to: *{escape_markdown_v2(lang_code)}*"
    )


@user_router.message(Command("my_lang"))
async def handle_my_lang(message: Message):
    lang = await Database.get_user_ocr_language(message.from_user.id)
    await message.reply(f"Your current OCR language is: *{escape_markdown_v2(lang)}*")


@user_router.message(Command("limits"))
async def handle_limits(message: Message):
    limiter = RateLimiter(message.from_user.id)
    usage_info = await limiter.get_current_usage_info()
    await message.reply(escape_markdown_v2(usage_info))


@user_router.message(F.photo)
async def handle_photo(message: Message, bot: Bot):
    user_id = message.from_user.id
    logger.info(f"Received photo from user {user_id}")

    if user_id != ADMIN_ID:
        limiter = RateLimiter(user_id)
        is_allowed, limit_message = await limiter.check_limit()
        if not is_allowed:
            await message.reply(escape_markdown_v2(limit_message))
            return

    photo: PhotoSize = message.photo[-1]
    engine_name = await Database.get_user_ocr_preference(user_id)
    language = await Database.get_user_ocr_language(user_id)
    ocr_engine = get_ocr_engine(engine_name)

    processing_msg = await message.reply(
        f"Processing with *{escape_markdown_v2(engine_name)}* \\(lang: *{escape_markdown_v2(language)}*\\)\\.\\.\\."
    )

    temp_image_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_image_path = Path(temp_file.name)
            await bot.download(file=photo.file_id, destination=temp_image_path)
            logger.debug(f"Photo downloaded to {temp_image_path}")

        recognized_text = await ocr_engine.recognize(temp_image_path, language=language)

        if not recognized_text or not recognized_text.strip():
            await processing_msg.edit_text(
                "Could not recognize any text from the image\\."
            )
            return

        if user_id != ADMIN_ID:
            await Database.log_usage(user_id, engine_name)

        text_to_send = escape_markdown_v2(recognized_text.strip())
        max_len = 4000

        header = f"*Recognized Text \\({escape_markdown_v2(engine_name)}\\):*\n"
        full_message = f"{header}```\n{text_to_send}\n```"

        if len(full_message) <= max_len:
            await processing_msg.edit_text(full_message)
        else:
            await processing_msg.edit_text(header)
            for i in range(0, len(text_to_send), max_len):
                chunk = text_to_send[i : i + max_len]
                await message.reply(f"```\n{chunk}\n```")

    except Exception as e:
        logger.exception(f"Error handling photo for user {user_id}: {e}")
        await processing_msg.edit_text(
            "An error occurred while processing your image\\. Please try again later\\."
        )
    finally:
        if temp_image_path and temp_image_path.exists():
            os.remove(temp_image_path)
            logger.debug(f"Temporary file {temp_image_path} deleted.")


def register_user_handlers(dp: Router):
    dp.include_router(user_router)
