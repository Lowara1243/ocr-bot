import pytest_asyncio
from dotenv import load_dotenv
from pathlib import Path

from src.ocr_bot.database.db import Database
from src.ocr_bot.ocr_engines.tesseract_ocr import TesseractOCR
from src.ocr_bot.ocr_engines.yandex_ocr import YandexOCR


def pytest_configure(config):
    """
    Hook to configure pytest before tests are collected and modules are imported.
    Loads environment variables from .env.test for testing.
    """
    env_path = Path(__file__).parent / ".env.test"
    load_dotenv(dotenv_path=env_path)


@pytest_asyncio.fixture
async def db(mocker):
    """
    Fixture to set up and tear down the in-memory database for each test function.
    """
    mocker.patch("src.ocr_bot.database.db.DATABASE_PATH", ":memory:")
    await Database.init_db()
    yield
    await Database.close_connection()


@pytest_asyncio.fixture
async def tesseract_ocr():
    """
    Fixture to provide a TesseractOCR instance for tests.
    """
    return TesseractOCR()


@pytest_asyncio.fixture
async def yandex_ocr():
    """
    Fixture to provide a YandexOCR instance for tests.
    """
    return YandexOCR()
