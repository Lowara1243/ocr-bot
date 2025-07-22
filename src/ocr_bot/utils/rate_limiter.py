from datetime import datetime, timedelta

from loguru import logger

from src.ocr_bot.config import RATE_LIMIT_DAILY, RATE_LIMIT_WEEKLY, RATE_LIMIT_MONTHLY
from src.ocr_bot.database.db import Database


def _get_start_of_current_month_ts() -> int:
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(start_of_month.timestamp())


def _get_start_of_current_day_ts() -> int:
    now = datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(start_of_day.timestamp())


def _get_start_of_current_week_ts() -> int:
    now = datetime.now()
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(start_of_week.timestamp())


class RateLimiter:
    def __init__(self, user_id: int):
        self.user_id = user_id

    async def check_limit(self) -> tuple[bool, str]:
        """
        Checks if the user has exceeded the limits.
        Returns: (allowed_level, message)
        """
        daily_start_ts = _get_start_of_current_day_ts()

        daily_count = await Database.get_usage_counts(self.user_id, daily_start_ts)
        if daily_count >= RATE_LIMIT_DAILY:
            msg = f"Daily limit of {RATE_LIMIT_DAILY} requests reached. Try again tomorrow."
            logger.warning(f"User {self.user_id}: {msg}")
            return False, msg

        weekly_start_ts = _get_start_of_current_week_ts()

        weekly_count = await Database.get_usage_counts(self.user_id, weekly_start_ts)
        if weekly_count >= RATE_LIMIT_WEEKLY:
            msg = f"Weekly limit of {RATE_LIMIT_WEEKLY} requests reached. Try again next week."
            logger.warning(f"User {self.user_id}: {msg}")
            return False, msg

        monthly_start_ts = _get_start_of_current_month_ts()

        monthly_count = await Database.get_usage_counts(self.user_id, monthly_start_ts)
        if monthly_count >= RATE_LIMIT_MONTHLY:
            msg = f"Monthly limit of {RATE_LIMIT_MONTHLY} requests reached. Try again next month."
            logger.warning(f"User {self.user_id}: {msg}")
            return False, msg

        return True, "Limits OK"

    async def get_current_usage_info(self) -> str:
        daily_start_ts = _get_start_of_current_day_ts()

        daily_count = await Database.get_usage_counts(self.user_id, daily_start_ts)

        weekly_start_ts = _get_start_of_current_week_ts()

        weekly_count = await Database.get_usage_counts(self.user_id, weekly_start_ts)

        monthly_start_ts = _get_start_of_current_month_ts()

        monthly_count = await Database.get_usage_counts(self.user_id, monthly_start_ts)

        return (
            f"Your current usage:\n"
            f"- Daily: {daily_count}/{RATE_LIMIT_DAILY}\n"
            f"- Weekly: {weekly_count}/{RATE_LIMIT_WEEKLY}\n"
            f"- Monthly: {monthly_count}/{RATE_LIMIT_MONTHLY}"
        )
