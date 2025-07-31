import pytest
from pathlib import Path
import pytesseract


@pytest.mark.asyncio
async def test_recognize_success(tesseract_ocr, mocker):
    """Tests successful recognition without creating a real file."""
    # Arrange
    dummy_path = Path("dummy/path/to/image.jpg")
    mock_image_open = mocker.patch("src.ocr_bot.ocr_engines.tesseract_ocr.Image.open")
    mock_image_to_string = mocker.patch(
        "src.ocr_bot.ocr_engines.tesseract_ocr.pytesseract.image_to_string",
        return_value="Test text",
    )
    # Act
    result = await tesseract_ocr.recognize(dummy_path, language="eng")

    # Assert
    assert result == "Test text"
    mock_image_open.assert_called_once_with(dummy_path)
    mock_image_to_string.assert_called_once_with(
        mock_image_open.return_value, lang="eng"
    )


@pytest.mark.asyncio
async def test_recognize_tesseract_not_found(tesseract_ocr, mocker):
    """Tests the case where Tesseract is not found."""
    # Arrange
    dummy_path = Path("dummy.jpg")
    mocker.patch("src.ocr_bot.ocr_engines.tesseract_ocr.Image.open")
    mocker.patch(
        "src.ocr_bot.ocr_engines.tesseract_ocr.pytesseract.image_to_string",
        side_effect=pytesseract.TesseractNotFoundError,
    )
    # Act
    result = await tesseract_ocr.recognize(dummy_path)

    # Assert
    assert "Error: Tesseract OCR is not configured correctly on the server." in result


@pytest.mark.asyncio
async def test_recognize_runtime_error(tesseract_ocr, mocker):
    """Tests a runtime error during OCR, e.g., invalid language."""
    # Arrange
    dummy_path = Path("dummy.jpg")
    mocker.patch("src.ocr_bot.ocr_engines.tesseract_ocr.Image.open")
    mocker.patch(
        "src.ocr_bot.ocr_engines.tesseract_ocr.pytesseract.image_to_string",
        side_effect=RuntimeError("Invalid language"),
    )
    # Act
    result = await tesseract_ocr.recognize(dummy_path, language="invalid")

    # Assert
    assert "Error during Tesseract OCR: Invalid language" in result
    assert "Check if language 'invalid' is installed and valid" in result
