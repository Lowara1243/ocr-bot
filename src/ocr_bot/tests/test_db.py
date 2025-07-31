import pytest
import aiosqlite
import time

from src.ocr_bot.database.db import Database
from src.ocr_bot.config import DEFAULT_OCR_ENGINE, DEFAULT_OCR_LANGUAGE


@pytest.mark.asyncio
async def test_get_connection(db):
    """
    Test that a connection is established.
    """
    conn = await Database.get_connection()
    assert isinstance(conn, aiosqlite.Connection)


@pytest.mark.asyncio
async def test_init_db(db):
    """
    Test that the tables are created.
    """
    conn = await Database.get_connection()
    async with conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
    ) as cursor:
        assert await cursor.fetchone() is not None
    async with conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='usage_stats'"
    ) as cursor:
        assert await cursor.fetchone() is not None


@pytest.mark.asyncio
async def test_add_or_update_user(db):
    """
    Test adding a new user and updating an existing user.
    """
    # Add a new user
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    user = await Database._execute(
        "SELECT * FROM users WHERE user_id = ?", (1,), fetch="one"
    )
    assert user is not None
    assert user["username"] == "testuser"

    # Update the user
    await Database.add_or_update_user(1, "testuser_updated", "Test", "User")
    user = await Database._execute(
        "SELECT * FROM users WHERE user_id = ?", (1,), fetch="one"
    )
    assert user["username"] == "testuser_updated"


@pytest.mark.asyncio
async def test_get_user_ocr_preference(db):
    """
    Test getting the default and a custom OCR preference.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    # Test default preference
    preference = await Database.get_user_ocr_preference(1)
    assert preference == DEFAULT_OCR_ENGINE

    # Test custom preference
    await Database.set_user_ocr_preference(1, "custom_engine")
    preference = await Database.get_user_ocr_preference(1)
    assert preference == "custom_engine"


@pytest.mark.asyncio
async def test_get_user_ocr_preference_no_user(db):
    """
    Test getting the default OCR preference for a non-existent user.
    """
    preference = await Database.get_user_ocr_preference(999)
    assert preference == DEFAULT_OCR_ENGINE


@pytest.mark.asyncio
async def test_set_user_ocr_preference(db):
    """
    Test setting the OCR preference.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    await Database.set_user_ocr_preference(1, "new_engine")
    preference = await Database.get_user_ocr_preference(1)
    assert preference == "new_engine"


@pytest.mark.asyncio
async def test_get_user_ocr_language(db):
    """
    Test getting the default and a custom OCR language.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    # Test default language
    language = await Database.get_user_ocr_language(1)
    assert language == DEFAULT_OCR_LANGUAGE

    # Test custom language
    await Database.set_user_ocr_language(1, "eng")
    language = await Database.get_user_ocr_language(1)
    assert language == "eng"


@pytest.mark.asyncio
async def test_get_user_ocr_language_no_user(db):
    """
    Test getting the default OCR language for a non-existent user.
    """
    language = await Database.get_user_ocr_language(999)
    assert language == DEFAULT_OCR_LANGUAGE


@pytest.mark.asyncio
async def test_set_user_ocr_language(db):
    """
    Test setting the OCR language.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    await Database.set_user_ocr_language(1, "rus")
    language = await Database.get_user_ocr_language(1)
    assert language == "rus"


@pytest.mark.asyncio
async def test_log_usage(db):
    """
    Test logging a usage event.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    await Database.log_usage(1, "test_engine")
    usage = await Database._execute(
        "SELECT * FROM usage_stats WHERE user_id = ?", (1,), fetch="one"
    )
    assert usage is not None
    assert usage["engine_used"] == "test_engine"


@pytest.mark.asyncio
async def test_get_usage_counts(db):
    """
    Test counting usage events.
    """
    await Database.add_or_update_user(1, "testuser", "Test", "User")
    current_time = int(time.time())
    await Database.log_usage(1, "test_engine")
    await Database.log_usage(1, "test_engine")
    count = await Database.get_usage_counts(1, current_time - 60)
    assert count == 2
    count = await Database.get_usage_counts(1, current_time + 60)
    assert count == 0


@pytest.mark.asyncio
async def test_execute_fetchall(db):
    """
    Test the _execute method with fetch='all'.
    """
    await Database.add_or_update_user(1, "testuser1", "Test", "User")
    await Database.add_or_update_user(2, "testuser2", "Test", "User")
    users = await Database._execute("SELECT * FROM users", fetch="all")
    assert len(users) == 2


@pytest.mark.asyncio
async def test_execute_error(db):
    """
    Test that _execute raises an exception on error.
    """
    with pytest.raises(aiosqlite.Error):
        await Database._execute("SELECT * FROM non_existent_table")
