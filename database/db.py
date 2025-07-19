import aiosqlite
import time
from typing import Optional, Any

from loguru import logger

from config import DATABASE_PATH, DEFAULT_OCR_ENGINE, DEFAULT_OCR_LANGUAGE

class Database:
    _conn: Optional[aiosqlite.Connection] = None

    @classmethod
    async def get_connection(cls) -> aiosqlite.Connection:
        if cls._conn is None:
            try:
                logger.info(f"Connecting to database at {DATABASE_PATH}")
                cls._conn = await aiosqlite.connect(DATABASE_PATH)
                cls._conn.row_factory = aiosqlite.Row
            except aiosqlite.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return cls._conn

    @classmethod
    async def close_connection(cls):
        if cls._conn:
            await cls._conn.close()
            cls._conn = None
            logger.info("Database connection closed.")

    @classmethod
    async def _execute(cls, sql: str, params: tuple = (), fetch: str = None) -> Any:
        """
        Universal method for executing SQL queries.
        :param sql: SQL query.
        :param params: Parameters for the query.
        :param fetch: Fetch type: ‘one’, ‘all’ or None for commit. Error
        """
        try:
            conn = await cls.get_connection()
            async with conn.cursor() as cursor:
                await cursor.execute(sql, params)
                if fetch == 'one':
                    return await cursor.fetchone()
                if fetch == 'all':
                    return await cursor.fetchall()
                await conn.commit()
        except aiosqlite.Error as e:
            logger.error(f"Database query error: {e}\nSQL: {sql}\nParams: {params}")
            raise

    @classmethod
    async def init_db(cls):
        default_engine_sql = DEFAULT_OCR_ENGINE.replace("'", "''")
        default_language_sql = DEFAULT_OCR_LANGUAGE.replace("'", "''")
        await cls._execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                ocr_engine_preference TEXT DEFAULT '{default_engine_sql}',
                ocr_language_preference TEXT DEFAULT '{default_language_sql}',
                created_at INTEGER,
                last_active_at INTEGER
            )
        """)
        await cls._execute("""
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp INTEGER,
                engine_used TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        logger.info("Database initialized successfully.")

    @classmethod
    async def add_or_update_user(cls, user_id: int, username: Optional[str], first_name: Optional[str], last_name: Optional[str]):
        current_time = int(time.time())
        sql = """
            INSERT INTO users (user_id, username, first_name, last_name, created_at, last_active_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username=excluded.username,
                first_name=excluded.first_name,
                last_name=excluded.last_name,
                last_active_at=excluded.last_active_at
        """
        params = (user_id, username, first_name, last_name, current_time, current_time)
        await cls._execute(sql, params)
        logger.debug(f"User {user_id} added or updated.")

    @classmethod
    async def get_user_ocr_preference(cls, user_id: int) -> str:
        result = await cls._execute("SELECT ocr_engine_preference FROM users WHERE user_id = ?", (user_id,), fetch='one')
        return result['ocr_engine_preference'] if result and result['ocr_engine_preference'] else DEFAULT_OCR_ENGINE

    @classmethod
    async def set_user_ocr_preference(cls, user_id: int, engine_name: str):
        await cls._execute("UPDATE users SET ocr_engine_preference = ? WHERE user_id = ?", (engine_name, user_id))
        logger.info(f"User {user_id} OCR engine preference set to {engine_name}.")

    @classmethod
    async def get_user_ocr_language(cls, user_id: int) -> str:
        result = await cls._execute("SELECT ocr_language_preference FROM users WHERE user_id = ?", (user_id,), fetch='one')
        return result['ocr_language_preference'] if result and result['ocr_language_preference'] else DEFAULT_OCR_LANGUAGE

    @classmethod
    async def set_user_ocr_language(cls, user_id: int, language_code: str):
        await cls._execute("UPDATE users SET ocr_language_preference = ? WHERE user_id = ?", (language_code, user_id))
        logger.info(f"User {user_id} OCR language preference set to {language_code}.")

    @classmethod
    async def log_usage(cls, user_id: int, engine_used: str):
        current_time = int(time.time())
        await cls._execute("INSERT INTO usage_stats (user_id, timestamp, engine_used) VALUES (?, ?, ?)", (user_id, current_time, engine_used))
        logger.debug(f"Usage logged for user {user_id} with engine {engine_used}.")

    @classmethod
    async def get_usage_counts(cls, user_id: int, since_timestamp: int) -> int:
        sql = "SELECT COUNT(*) FROM usage_stats WHERE user_id = ? AND timestamp >= ?"
        params = (user_id, since_timestamp)
        result = await cls._execute(sql, params, fetch='one')
        return result[0] if result else 0
