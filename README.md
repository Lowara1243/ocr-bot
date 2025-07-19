[English](README.md) | [Русский](README.ru.md)

---

# Telegram OCR Bot

A Telegram bot that uses Tesseract or Yandex Vision to transcribe text from images.

## Table of Contents
- [Features](#features)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
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
This is the recommended way to run the bot.

1.  Create a new directory for your bot.
2.  Create a `docker-compose.yml` file in this directory with the following content:
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
3.  **Configure the bot.** At a minimum, you need to create a `.env` file and set your `BOT_TOKEN`. See the [Configuration](#configuration) section for a full guide and list of all variables.
4.  Run the bot:
    ```bash
    docker-compose up -d
    ```
5.  The bot will start and connect to Telegram using your token.

## Installation from Source
<details>
<summary>Click to expand for manual installation instructions</summary>

1.  **Clone the repository**
    ```bash
    git clone https://github.com/Lowara1243/ocr-bot.git
    cd ocr-bot
    ```
2.  **Create a virtual environment & install dependencies**
    - Using `uv` (recommended):
        ```bash
        uv pip install -r requirements.txt
        ```
    - Using standard `pip`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate     # For Windows use: .venv\Scripts\activate
        pip install -r requirements.txt
        ```
3.  **Configure the bot.** Create a `.env` file and set your `BOT_TOKEN` and any other required variables. See the [Configuration](#configuration) section for details.
4.  **Run the bot**
    ```bash
    python main.py
    ```
    </details>

## Configuration
To configure the bot, create a `.env` file in the project's root directory. The easiest way is to copy the example file:

```bash
cp .env.example .env
```

Then, open `.env` in your editor and adjust the settings.

| Variable                  | Description                                                          | Required |
|:--------------------------|:---------------------------------------------------------------------|:--------:|
| `BOT_TOKEN`               | Your Telegram bot token from [@BotFather](https://t.me/BotFather).   | **Yes**  |
| `ADMIN_ID`                | Your Telegram User ID (admin has no limits).                         |    No    |
| `DEFAULT_OCR_ENGINE`      | Default OCR engine to use (`tesseract` or `yandex`).                 |    No    |
| `ENABLED_OCR_ENGINES`     | Comma-separated list of enabled engines (e.g., `tesseract,yandex`).  |    No    |
| `YANDEX_CLOUD_API_KEY`    | API key for Yandex Cloud Vision API.                                 |    No    |
| `YANDEX_CLOUD_FOLDER_ID`  | Folder ID for Yandex Cloud Vision API.                               |    No    |
| `RATE_LIMIT_DAILY`        | Daily request limit (integer).                                       |    No    |
| `RATE_LIMIT_WEEKLY`       | Weekly request limit (integer).                                      |    No    |
| `RATE_LIMIT_MONTHLY`      | Monthly request limit (integer).                                     |    No    |
| `LOG_LEVEL`               | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.      |    No    |
| `LOG_FILE`                | Path to the log file (leave empty to log to console only).           |    No    |
| `DATABASE_PATH`           | Path to the SQLite database file (e.g., `database/ocr_bot.db`).      |    No    |
| `TESSERACT_CMD_PATH`      | Full path to the `tesseract` executable if not in the system `PATH`. |    No    |
| `DEFAULT_OCR_LANGUAGE`    | Default OCR language (`eng`, `rus`, `eng+rus`, etc.).                |    No    |
| `SUPPORTED_OCR_LANGUAGES` | Comma-separated list of supported languages (for Tesseract).         |    No    |
| `OCR_LOG_PREVIEW_LENGTH`  | Number of characters to preview from transcribed text in logs.       |    No    |

## Bot Management
- **View logs:**  
  ```bash
  docker-compose logs -f
  ```

- **Stop the bot:**
  ```bash
  docker-compose down
  ```

- **Restart the bot:**
  ```bash
  docker-compose restart
  ```