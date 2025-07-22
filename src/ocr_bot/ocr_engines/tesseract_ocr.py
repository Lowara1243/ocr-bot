import pytesseract
from PIL import Image
from pathlib import Path
from loguru import logger
from typing import Optional

from .base_ocr import BaseOCR
from src.ocr_bot.config import TESSERACT_CMD_PATH, OCR_LOG_PREVIEW_LENGTH

if TESSERACT_CMD_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD_PATH


class TesseractOCR(BaseOCR):
    async def recognize(self, image_path: Path, language: Optional[str] = None) -> str:
        try:
            lang_param = language if language else None
            logger.info(
                f"Processing image with Tesseract: {image_path}, Language: {lang_param or 'default'}"
            )

            text = pytesseract.image_to_string(Image.open(image_path), lang=lang_param)

            preview_text = text[:OCR_LOG_PREVIEW_LENGTH].replace(chr(10), " ")
            logger.info(
                f"Tesseract recognized text (first {OCR_LOG_PREVIEW_LENGTH} chars): {preview_text}"
            )
            return text.strip()
        except pytesseract.TesseractNotFoundError:
            logger.error("Tesseract is not installed or not in your PATH.")
            logger.error(
                "Please install Tesseract and/or set TESSERACT_CMD_PATH in .env"
            )
            return "Error: Tesseract OCR is not configured correctly on the server."
        except RuntimeError as e:
            logger.error(
                f"Error during Tesseract OCR processing (possibly invalid language '{language}'): {e}"
            )
            return f"Error during Tesseract OCR: {str(e)}. Check if language '{language}' is installed and valid."
        except Exception as e:
            logger.error(f"Error during Tesseract OCR processing: {e}")
            return f"Error during Tesseract OCR: {str(e)}"
