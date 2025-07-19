[English](README.md) | [Русский](README.ru.md)
---

# Telegram OCR Bot

A Telegram bot that uses Tesseract or Yandex Vision to transcribe text from images.

## Table of Contents
- [Features](#features)
- [Quick Start (Docker Compose)](#quick-start-docker)
- [Installation from Source](#installation-from-source)
- [Configuration](#configuration)
- [Bot Management](#bot-management)

## Features

-   Transcribes text from images sent as photos.
-   **Multiple OCR Engines:** Supports local processing with **Tesseract** and cloud-based with **Yandex Vision**.
-   **Persistent Storage:** Uses SQLite to store user data and settings.
-   **Flexible Limits System:** Includes configurable daily, weekly, and monthly usage limits.
-   **Ready for Deployment:** Optimized for easy deployment with Docker Compose / Podman Compose.

## Quick Start (Docker)

This is the fastest way to get the bot running if you don't want to build the image from source.

1.  **Create an `.env` file** in a new directory with your `BOT_TOKEN` and other necessary variables (see the "Setup and Installation" section for details).

2.  **Create a `docker-compose.yml` file** in the same directory.
    
    **Note:** This version uses the `image:` directive instead of `build: .`. Make sure to replace `YOUR_USERNAME` with the actual username where the image is hosted.

    ```yaml
    version: '3.8'

    services:
      ocr-bot:
        # Use the pre-built image from Docker Hub
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

3.  **Run the container:**
    ```bash
    docker-compose up -d
    ```
The bot will start using the pre-built image from Docker Hub.

## Installation from Source

<details>
<summary>Click to expand instructions for manual installation</summary>

This method is suitable for development or if you prefer not to use Docker.

**1. Clone the repository**
```bash
git clone https://github.com/Lowara1243/ocr-bot.git
cd ocr-bot
```

**2. Create a virtual environment and install dependencies**

*   **Using `uv` (recommended):**
    ```bash
    uv pip install -r requirements.txt
    ```
*   **Using `pip`:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

**3. Configure environment variables**

Copy `.env.example` to `.env` and fill in your values, especially `BOT_TOKEN`.
```bash
cp .env.example .env
```
> For a description of all variables, see the [Configuration](#configuration) section.

**4. Run the bot**
```bash
python main.py
```

</details>

## Configuration

The bot is configured using environment variables located in the `.env` file.

| Variable           | Description                                                                            | Required |
|:-------------------|:---------------------------------------------------------------------------------------|:--------:|
| `BOT_TOKEN`        | Your Telegram bot token from [@BotFather](https://t.me/BotFather).                     | **Yes**  |
| `ADMIN_ID`         | Your personal Telegram User ID. The admin has no usage limits.                         |    No    |
| `YANDEX_API_KEY`   | Your Yandex Cloud API Key for the Yandex Vision engine.                                |    No    |
| `YANDEX_FOLDER_ID` | Your Yandex Cloud Folder ID for the Yandex Vision engine.                              |    No    |
| `DB_FILENAME`      | The name of the SQLite database file. It will be created in the `database/` directory. |    No    |
| `LOG_LEVEL`        | Logging level: `INFO`, `DEBUG`, `WARNING`, `ERROR`.                                    |    No    |


## Bot Management

- **View logs:** `docker-compose logs -f`
- **Stop the bot:** `docker-compose down`
- **Restart the bot:** `docker-compose restart`