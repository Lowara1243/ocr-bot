[English](README.md) | [Русский](README.ru.md)

---

# Telegram OCR Bot

A Telegram bot that uses Tesseract or Yandex Vision to transcribe text from images.

## Table of Contents
- [Features](#features)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
- [Setup and Installation](#setup-and-installation)
- [Installation from Source](#installation-from-source)
- [Configuration](#configuration)
- [Bot Management](#bot-management)

## Features
- Transcribes text from images sent as photos.
- **Multiple OCR Engines:** Supports local processing with **Tesseract** and cloud-based with **Yandex Vision**.
- **Persistent Storage:** Uses SQLite to store user data and settings.
- **Flexible Limits System:** Configurable daily, weekly, and monthly usage limits.
- **Ready for Deployment:** Optimized for easy deployment with Docker Compose / Podman Compose.

## Quick Start (Docker Compose)
1. Create a new directory and place your `docker-compose.yml` there.
2. Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
3. Edit `.env` and set at least `BOT_TOKEN`.
4. Create a `docker-compose.yml` with the following content, replacing `YOUR_USERNAME` if you host the image yourself:
    ```yaml
    version: '3.8'

    services:
      ocr-bot:
        image: lowara1243/ocr-bot:1.0
        container_name: telegram_ocr_bot
        restart: always
        env_file:
          - .env
        volumes:
          - ./database:/app/database
          - ./logs:/app/logs
          - ./temp_images:/app/temp_images
        tty: true
    ```
5. Run:
    ```bash
    docker-compose up -d
    ```
6. The bot will start and connect to Telegram using your token.

## Setup and Installation
Before first run, complete the following:

1. Copy the example `.env`:
    ```bash
    cp .env.example .env
    ```
2. Open `.env` in your editor and fill in:
   - `BOT_TOKEN` — your Telegram bot token from [@BotFather](https://t.me/BotFather).
3. (Optional) Adjust other settings as needed:
   - `ADMIN_ID` — your Telegram User ID (admin without limits).
   - `DEFAULT_OCR_ENGINE` — default OCR engine (`tesseract` or `yandex`).
   - `ENABLED_OCR_ENGINES` — comma-separated list of enabled engines (e.g. `tesseract,yandex`).
   - `YANDEX_CLOUD_API_KEY` / `YANDEX_CLOUD_FOLDER_ID` — for Yandex Vision API.
   - `RATE_LIMIT_DAILY`, `RATE_LIMIT_WEEKLY`, `RATE_LIMIT_MONTHLY` — numeric rate limits.
   - `LOG_LEVEL` — `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
   - `LOG_FILE` — path to log file (empty = console only).
   - `DATABASE_PATH` — path to SQLite file (e.g. `database/ocr_bot.db`).
   - `TESSERACT_CMD_PATH` — full path to `tesseract`, if not in system `PATH`.
   - `DEFAULT_OCR_LANGUAGE` / `SUPPORTED_OCR_LANGUAGES` — OCR language codes.
   - `OCR_LOG_PREVIEW_LENGTH` — number of characters to preview in logs.
4. Start the container:
    ```bash
    docker-compose up -d
    ```

For full descriptions of all variables, see [Configuration](#configuration).

## Installation from Source
<details>
<summary>Click to expand manual installation</summary>

1. **Clone the repository**
    ```bash
    git clone https://github.com/Lowara1243/ocr-bot.git
    cd ocr-bot
    ```
2. **Create virtual environment & install dependencies**
    - Using `uv` (recommended):
        ```bash
        uv pip install -r requirements.txt
        ```
    - Using standard `pip`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate     # Windows: .venv\Scripts\activate
        pip install -r requirements.txt
        ```
3. **Configure environment**
    ```bash
    cp .env.example .env
    ```
    Fill in at least `BOT_TOKEN`; see [Configuration](#configuration) for details.
4. **Run the bot**
    ```bash
    python main.py
    ```
</details>

## Configuration
Copy `.env.example` to `.env` and adjust:

| Переменная                | Описание                                                              | Обязательно |
|:--------------------------|:----------------------------------------------------------------------|:-----------:|
| `BOT_TOKEN`               | Ваш Telegram-бот токен от [@BotFather](https://t.me/BotFather).       |   **Да**    |
| `ADMIN_ID`                | Ваш Telegram User ID (админ без ограничений).                         |     Нет     |
| `DEFAULT_OCR_ENGINE`      | Движок OCR по умолчанию (`tesseract` или `yandex`).                   |     Нет     |
| `ENABLED_OCR_ENGINES`     | Список движков через запятую (например, `tesseract,yandex`).          |     Нет     |
| `YANDEX_CLOUD_API_KEY`    | API-ключ Yandex Cloud для Yandex Vision API.                          |     Нет     |
| `YANDEX_CLOUD_FOLDER_ID`  | ID папки в Yandex Cloud для Yandex Vision API.                        |     Нет     |
| `RATE_LIMIT_DAILY`        | Суточный лимит запросов (целое число).                                |     Нет     |
| `RATE_LIMIT_WEEKLY`       | Недельный лимит запросов (целое число).                               |     Нет     |
| `RATE_LIMIT_MONTHLY`      | Месячный лимит запросов (целое число).                                |     Нет     |
| `LOG_LEVEL`               | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |     Нет     |
| `LOG_FILE`                | Имя файла логов (оставьте пустым для консоли).                        |     Нет     |
| `DATABASE_PATH`           | Путь до SQLite-файла (например `database/ocr_bot.db`).                |     Нет     |
| `TESSERACT_CMD_PATH`      | Полный путь к `tesseract`, если не в системном `PATH`.                |     Нет     |
| `DEFAULT_OCR_LANGUAGE`    | Язык OCR по умолчанию (`eng`, `rus`, `eng+rus` и т.п.).               |     Нет     |
| `SUPPORTED_OCR_LANGUAGES` | Поддерживаемые языки через запятую (для Tesseract).                   |     Нет     |
| `OCR_LOG_PREVIEW_LENGTH`  | Длина предпросмотра текста в логах (в символах).                      |     Нет     |

## Bot Management
- **View logs:**  
  ```bash
  docker-compose logs -f
  ```

* **Stop the bot:**

  ```bash
  docker-compose down
  ```
* **Restart the bot:**

  ```bash
  docker-compose restart
  ```
