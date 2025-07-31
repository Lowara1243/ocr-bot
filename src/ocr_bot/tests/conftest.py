import pytest_asyncio

from src.ocr_bot.database.db import Database
from src.ocr_bot.ocr_engines.tesseract_ocr import TesseractOCR
from src.ocr_bot.ocr_engines.yandex_ocr import YandexOCR


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
