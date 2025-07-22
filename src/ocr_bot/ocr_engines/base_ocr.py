from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseOCR(ABC):
    @abstractmethod
    async def recognize(self, image_path: Path, language: Optional[str] = None) -> str:
        """
        Recognizes text from an image file.
        :param image_path: Path to the image file.
        :param language: Optional language code(s) for OCR (e.g., 'eng', 'rus', 'eng+rus').
        :return: Recognized text as a string.
        """
        pass
