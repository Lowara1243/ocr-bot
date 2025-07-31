import pytest
from src.ocr_bot.handlers.user_handlers import escape_markdown_v2


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Hello, world!", r"Hello, world\!"),
        ("_*[]()~`>#+-=|{}.\\!", r"\_\*\[\]\(\)\~\`\>\#\+\-\=\|\{\}\.\\!"),
        ("This is a test.", r"This is a test\."),
        ("1+1=2", r"1\+1\=2"),
        ("No special characters here", "No special characters here"),
        ("", ""),
    ],
)
def test_escape_markdown_v2(input_text, expected_output):
    assert escape_markdown_v2(input_text) == expected_output
