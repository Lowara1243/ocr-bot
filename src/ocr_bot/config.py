from pathlib import Path
from environs import Env

env = Env()
env.read_env()

# Bot
BOT_TOKEN = env.str("BOT_TOKEN")

# Admin ID
ADMIN_ID = env.int("ADMIN_ID", None)

# OCR
DEFAULT_OCR_ENGINE = env.str("DEFAULT_OCR_ENGINE", "tesseract")
TESSERACT_CMD_PATH = env.str("TESSERACT_CMD_PATH", None)

# OCR Language Settings
DEFAULT_OCR_LANGUAGE = env.str("DEFAULT_OCR_LANGUAGE", "eng")
# environs умеет парсить списки
SUPPORTED_OCR_LANGUAGES = env.list("SUPPORTED_OCR_LANGUAGES", default=["eng", "rus"])

# API Keys
YANDEX_CLOUD_API_KEY = env.str("YANDEX_CLOUD_API_KEY", None)
YANDEX_CLOUD_FOLDER_ID = env.str("YANDEX_CLOUD_FOLDER_ID", None)

# Rate Limits (автоматическое преобразование в int)
RATE_LIMIT_DAILY = env.int("RATE_LIMIT_DAILY", 100)
RATE_LIMIT_WEEKLY = env.int("RATE_LIMIT_WEEKLY", 500)
RATE_LIMIT_MONTHLY = env.int("RATE_LIMIT_MONTHLY", 1500)

# Logging
LOG_LEVEL = env.str("LOG_LEVEL", "INFO").upper()
OCR_LOG_PREVIEW_LENGTH = env.int("OCR_LOG_PREVIEW_LENGTH", 50)

# Database
DATABASE_FOLDER = "database"
Path(DATABASE_FOLDER).mkdir(parents=True, exist_ok=True)
DATABASE_FILENAME = env.str("DATABASE_FILENAME", "ocr_bot.db")
DATABASE_PATH = f"{DATABASE_FOLDER}/{DATABASE_FILENAME}"

# Available OCR Engines
ENABLED_OCR_ENGINES = env.list("ENABLED_OCR_ENGINES", default=["tesseract"])
