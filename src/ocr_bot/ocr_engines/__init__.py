import os
from ..config import ENABLED_OCR_ENGINES
from .base_ocr import BaseOCR
from .tesseract_ocr import TesseractOCR
from .yandex_ocr import YandexOCR

ALL_ENGINES = {
    "tesseract": TesseractOCR,
    "yandex": YandexOCR,
}

ENGINES = {}


def initialize_engines():
    for engine_name in ENABLED_OCR_ENGINES:
        engine_name = engine_name.lower()
        if engine_name in ALL_ENGINES:
            try:
                engine_class = ALL_ENGINES[engine_name]
                engine_instance = engine_class()

                if engine_name == "yandex":
                    if not os.getenv("YANDEX_CLOUD_API_KEY") or not os.getenv(
                        "YANDEX_CLOUD_FOLDER_ID"
                    ):
                        print(
                            "Warning: Yandex OCR engine is enabled but required API key or folder ID is not configured in .env. Skipping."
                        )
                        continue

                ENGINES[engine_name] = engine_instance
                print(f"Successfully initialized OCR engine: {engine_name}")
            except Exception as e:
                print(f"Error initializing OCR engine {engine_name}: {e}")


initialize_engines()


def get_ocr_engine(engine_name: str) -> BaseOCR:
    engine = ENGINES.get(engine_name.lower())
    if not engine:
        raise ValueError(
            f"Unsupported or disabled OCR engine: {engine_name}. Available and configured: {list(ENGINES.keys())}"
        )
    return engine
