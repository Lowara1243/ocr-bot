import pytest
from pathlib import Path
import httpx


@pytest.mark.asyncio
async def test_recognize_success(yandex_ocr, httpx_mock, mocker):
    httpx_mock.add_response(
        method="POST",
        url=yandex_ocr.ENDPOINT,
        json={
            "results": [
                {
                    "results": [
                        {
                            "textDetection": {
                                "pages": [
                                    {
                                        "blocks": [
                                            {
                                                "lines": [
                                                    {
                                                        "words": [
                                                            {"text": "Test"},
                                                            {"text": "text"},
                                                        ]
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        },
    )
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"test"))
    result = await yandex_ocr.recognize(Path("dummy.jpg"), language="eng")
    assert result == "Test text"


@pytest.mark.asyncio
async def test_recognize_http_error(yandex_ocr, httpx_mock, mocker):
    httpx_mock.add_response(status_code=500)
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"test"))
    result = await yandex_ocr.recognize(Path("dummy.jpg"))
    assert "Yandex OCR HTTP Error" in result


@pytest.mark.asyncio
async def test_recognize_request_error(yandex_ocr, httpx_mock, mocker):
    httpx_mock.add_exception(httpx.RequestError("test error"))
    mocker.patch("builtins.open", mocker.mock_open(read_data=b"test"))
    result = await yandex_ocr.recognize(Path("dummy.jpg"))
    assert "Yandex OCR connection Error" in result
