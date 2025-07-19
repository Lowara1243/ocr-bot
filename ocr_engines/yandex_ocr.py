import base64
import httpx
from pathlib import Path
from loguru import logger
from typing import Optional, Dict

from .base_ocr import BaseOCR
from config import YANDEX_CLOUD_API_KEY, YANDEX_CLOUD_FOLDER_ID

class YandexOCR(BaseOCR):
    ENDPOINT = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"
    LANG_MAP = {
        "eng": "en",
        "rus": "ru",
        "deu": "de",
        "fra": "fr",
        "spa": "sp",
    }

    def __init__(self):
        self.api_key = YANDEX_CLOUD_API_KEY
        self.folder_id = YANDEX_CLOUD_FOLDER_ID
        self.http_client = httpx.AsyncClient(timeout=60.0)

    def _build_request_payload(self, image_b64: str, language: Optional[str]) -> Dict:
        if language and self.LANG_MAP.get(language):
            language_codes = [self.LANG_MAP[language]]
        else:
            language_codes = ["*"]

        return {
            "folderId": self.folder_id,
            "analyzeSpecs": [{
                "content": image_b64,
                "features": [{
                    "type": "TEXT_DETECTION",
                    "textDetectionConfig": {
                        "languageCodes": language_codes
                    }
                }],
            }]
        }

    def _parse_response(self, data: Dict) -> str:
        try:
            pages = data['results'][0]['results'][0]['textDetection']['pages']

            all_blocks_text = []
            for page in pages:
                for block in page.get('blocks', []):
                    all_lines_text = []
                    for line in block.get('lines', []):
                        line_text = " ".join(word.get('text', '') for word in line.get('words', []))
                        all_lines_text.append(line_text)

                    block_text = "\n".join(all_lines_text)
                    all_blocks_text.append(block_text)

            full_text = "\n\n".join(all_blocks_text).strip()

            return full_text if full_text else "[Yandex OCR: text not found]"

        except (KeyError, IndexError) as e:
            logger.error(f"Could not parse Yandex API response structure. Error: {e}. Response: {data}")
            return "[Yandex OCR: response parsing error]"

    async def recognize(self, image_path: Path, language: Optional[str] = None) -> str:
        try:
            with open(image_path, "rb") as image_file:
                img_b64 = base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            logger.error(f"Could not read image file {image_path}: {e}")
            return f"[File read error: {e}]"

        request_body = self._build_request_payload(img_b64, language)
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = await self.http_client.post(self.ENDPOINT, json=request_body, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Yandex API response: {data}")

            return self._parse_response(data)

        except httpx.HTTPStatusError as e:
            logger.exception("Yandex OCR HTTP error")
            error_details = e.response.text
            return f"[Yandex OCR HTTP Error: {e.response.status_code} - {error_details}]"
        except httpx.RequestError as e:
            logger.exception("Yandex OCR Request error")
            return f"[Yandex OCR connection Error: {e}]"
        except Exception as e:
            logger.exception("Yandex OCR unexpected error")
            return f"[Yandex OCR unforeseen exception: {e}]"
