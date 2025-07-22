[English](README.md) | [Русский](README.ru.md)
---

# Telegram OCR Bot

<p align="center">
  <a href="https://github.com/Lowara1243/ocr-bot/actions/workflows/ci.yml"><img alt="CI Status" src="https://github.com/Lowara1243/ocr-bot/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/Lowara1243/ocr-bot/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/Lowara1243/ocr-bot"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Formatted with Ruff"></a>
</p>

A powerful Telegram bot that uses Tesseract or Yandex Vision to transcribe text from images. Built with Aiogram 3, asynchronous SQLite, and packaged for easy deployment with Docker.

---

## Table of Contents
- [Highlights](#-highlights)
- [Quick Start (Docker Compose)](#-quick-start-docker-compose)
- [Installation from Source](#-installation-from-source)
- [Configuration](#-configuration)
- [Bot Management](#-bot-management)
- [Contributing](#-contributing)
- [License](#-License)

## ✨ Highlights

-   **🚀 Multiple OCR Engines:** Supports local processing with **Tesseract** and powerful cloud-based recognition with **Yandex Vision**.
-   **⚡️ Asynchronous:** Built on `asyncio` and `aiogram` for high performance and responsiveness.
-   **💾 Persistent Storage:** Uses SQLite via `aiosqlite` to asynchronously store user data, settings, and usage statistics.
-   **⚙️ Flexible Limits System:** Easily configure daily, weekly, and monthly usage limits for users.
-   **🐳 Docker-Ready:** Optimized for one-command deployment using Docker Compose.
-   **🔧 Modern Tooling:** Uses `uv` for package management and `ruff` for linting and formatting, ensuring code quality.

## 🚀 Quick Start (Docker Compose)

This is the recommended way to run the bot for production.

1.  **Create a Project Directory:**
    Create a new directory and navigate into it.

2.  **Create `docker-compose.yml`:**
    Create a file named `docker-compose.yml` with the following content:

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
          - ./database:/app/src/ocr_bot/database
          - ./logs:/app/src/ocr_bot/logs
          - ./temp_images:/app/src/ocr_bot/temp_images
        tty: true
    ```
    > **Note:** Make sure you have created the local directories `./database`, `./logs`, and `./temp_images` before starting.

3.  **Configure the Bot:**
    Create a `.env` file in the same directory. At a minimum, you must provide your `BOT_TOKEN`. See the [Configuration](#-configuration) section for a full list of variables.

4.  **Run the Bot:**
    ```bash
    docker-compose up -d
    ```

The bot will start, create necessary files, and connect to Telegram.

## 🛠️ Installation from Source

<details>
<summary>Click to expand for manual installation instructions</summary>

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Lowara1243/ocr-bot.git
    cd ocr-bot
    ```

2.  **Install Dependencies:**
    We recommend using `uv`.
    ```bash
    # Will create .venv and install all dependencies from pyproject.toml
    uv pip install -e .
    ```

3.  **Configure the Bot:**
    Copy the example configuration file and edit it with your settings.
    ```bash
    cp .env.example .env
    nano .env
    ```

4.  **Run the Bot:**
    ```bash
    python src/ocr_bot/main.py
    ```
    </details>

## ⚙️ Configuration

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

## 🚦 Bot Management

Basic commands for managing the bot's Docker container.

-   **View logs:**
    ```bash
    docker-compose logs -f
    ```

-   **Stop the bot:**
    ```bash
    docker-compose down
    ```

-   **Restart the bot:**
    ```bash
    docker-compose restart
    ```


## 🤝 Contributing

Contributions are welcome! Whether it's bug reports, feature requests, or pull requests, all are appreciated.

-   **Found a bug?** Please use the [Bug Report](https://github.com/Lowara1243/ocr-bot/issues/new?assignees=&labels=bug&template=bug_report.yml&title=%5BBUG%5D+) template to submit an issue.
-   **Have a feature idea?** Open an issue to discuss it.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.