import pytest

from src.ocr_bot.config import (
    RATE_LIMIT_DAILY,
    RATE_LIMIT_WEEKLY,
    RATE_LIMIT_MONTHLY,
    ADMIN_ID,
)
from src.ocr_bot.utils.rate_limiter import RateLimiter


@pytest.fixture
def rate_limiter():
    return RateLimiter(user_id=1)


@pytest.mark.asyncio
async def test_check_limit_ok(mocker, rate_limiter):
    mocker.patch(
        "src.ocr_bot.utils.rate_limiter.Database.get_usage_counts", return_value=0
    )
    allowed, message = await rate_limiter.check_limit()
    assert allowed
    assert message == "Limits OK"


@pytest.mark.asyncio
async def test_check_limit_daily_exceeded(mocker, rate_limiter):
    mocker.patch(
        "src.ocr_bot.utils.rate_limiter.Database.get_usage_counts",
        return_value=RATE_LIMIT_DAILY,
    )
    allowed, message = await rate_limiter.check_limit()
    assert not allowed
    assert "Daily limit" in message


@pytest.mark.asyncio
async def test_check_limit_weekly_exceeded(mocker, rate_limiter):
    mocker.patch(
        "src.ocr_bot.utils.rate_limiter.Database.get_usage_counts",
        side_effect=[0, RATE_LIMIT_WEEKLY],
    )
    allowed, message = await rate_limiter.check_limit()
    assert not allowed
    assert "Weekly limit" in message


@pytest.mark.asyncio
async def test_check_limit_monthly_exceeded(mocker, rate_limiter):
    mocker.patch(
        "src.ocr_bot.utils.rate_limiter.Database.get_usage_counts",
        side_effect=[0, 0, RATE_LIMIT_MONTHLY],
    )
    allowed, message = await rate_limiter.check_limit()
    assert not allowed
    assert "Monthly limit" in message


@pytest.mark.asyncio
async def test_get_current_usage_info(mocker, rate_limiter):
    mocker.patch(
        "src.ocr_bot.utils.rate_limiter.Database.get_usage_counts",
        side_effect=[1, 2, 3],
    )
    usage_info = await rate_limiter.get_current_usage_info()
    assert f"Daily: 1/{RATE_LIMIT_DAILY}" in usage_info
    assert f"Weekly: 2/{RATE_LIMIT_WEEKLY}" in usage_info
    assert f"Monthly: 3/{RATE_LIMIT_MONTHLY}" in usage_info


@pytest.mark.asyncio
async def test_get_current_usage_info_admin():
    admin_limiter = RateLimiter(user_id=ADMIN_ID)
    usage_info = await admin_limiter.get_current_usage_info()
    assert "You have no limits because you're an admin" in usage_info
