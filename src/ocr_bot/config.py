import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path("../..") / ".env"
load_dotenv(dotenv_path=env_path)

# Bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file")

# OCR
DEFAULT_OCR_ENGINE = os.getenv("DEFAULT_OCR_ENGINE", "tesseract")
TESSERACT_CMD_PATH = os.getenv("TESSERACT_CMD_PATH")

# OCR Language Settings
DEFAULT_OCR_LANGUAGE = os.getenv("DEFAULT_OCR_LANGUAGE", "eng")
# Parse SUPPORTED_OCR_LANGUAGES into a list of strings
_supported_langs_str = os.getenv("SUPPORTED_OCR_LANGUAGES", "eng,rus")
SUPPORTED_OCR_LANGUAGES = [lang.strip() for lang in _supported_langs_str.split(",")]

# API Keys
YANDEX_CLOUD_API_KEY = os.getenv("YANDEX_CLOUD_API_KEY")
YANDEX_CLOUD_FOLDER_ID = os.getenv("YANDEX_CLOUD_FOLDER_ID")

# Rate Limits
RATE_LIMIT_DAILY = int(os.getenv("RATE_LIMIT_DAILY", 100))
RATE_LIMIT_WEEKLY = int(os.getenv("RATE_LIMIT_WEEKLY", 500))
RATE_LIMIT_MONTHLY = int(os.getenv("RATE_LIMIT_MONTHLY", 1500))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
OCR_LOG_PREVIEW_LENGTH = int(os.getenv("OCR_LOG_PREVIEW_LENGTH", 50))

# Database
DATABASE_FOLDER = "database"
Path(DATABASE_FOLDER).mkdir(parents=True, exist_ok=True)  # Ensure directory exists
DATABASE_FILENAME = os.getenv("DATABASE_FILENAME", "ocr_bot.db")
DATABASE_PATH = f"{DATABASE_FOLDER}/{DATABASE_FILENAME}"

# Available OCR Engines
ENABLED_OCR_ENGINES = [
    engine.strip()
    for engine in os.getenv("ENABLED_OCR_ENGINES", "tesseract").split(",")
]
