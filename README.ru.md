[English](README.md) | [Русский](README.ru.md)
---

# Telegram OCR Bot

<p align="center">
  <a href="https://github.com/Lowara1243/ocr-bot/actions/workflows/ci.yml"><img alt="Статус CI" src="https://github.com/Lowara1243/ocr-bot/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/Lowara1243/ocr-bot/blob/main/LICENSE"><img alt="Лицензия" src="https://img.shields.io/github/license/Lowara1243/ocr-bot"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Версия Python"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Форматирование с Ruff"></a>
</p>

Мощный Telegram бот, использующий Tesseract или Yandex Vision для распознавания текста на изображениях. Создан с использованием Aiogram 3, асинхронного SQLite и упакован для легкого развертывания с помощью Docker.

---

## Содержание
- [Ключевые особенности](#-ключевые-особенности)
- [Быстрый старт (Docker Compose)](#-быстрый-старт-docker-compose)
- [Установка из исходного кода](#-установка-из-исходного-кода)
- [Конфигурация](#-конфигурация)
- [Управление ботом](#-управление-ботом)
- [Участие в проекте](#-участие-в-проекте)
- [Лицензия](#-лицензия)

## ✨ Ключевые особенности

-   **🚀 Несколько OCR-движков:** Поддерживает локальную обработку с помощью **Tesseract** и мощное облачное распознавание с **Yandex Vision**.
-   **⚡️ Асинхронность:** Построен на `asyncio` и `aiogram` для высокой производительности и отзывчивости.
-   **💾 Постоянное хранилище:** Использует SQLite через `aiosqlite` для асинхронного хранения пользовательских данных, настроек и статистики использования.
-   **⚙️ Гибкая система лимитов:** Легко настраивайте дневные, недельные и месячные лимиты использования для пользователей.
-   **🐳 Готовность к Docker:** Оптимизирован для развертывания одной командой с помощью Docker Compose.
-   **🔧 Современные инструменты:** Использует `uv` для управления пакетами и `ruff` для линтинга и форматирования, обеспечивая качество кода.

## 🚀 Быстрый старт (Docker Compose)

Это рекомендуемый способ запуска бота для производственного использования.

1.  **Создайте директорию проекта:**
    Создайте новую директорию и перейдите в нее.

2.  **Создайте `docker-compose.yml`:**
    Создайте файл с именем `docker-compose.yml` со следующим содержимым:

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
    > **Примечание:** Перед запуском убедитесь, что вы создали локальные директории `./database`, `./logs` и `./temp_images`.

3.  **Настройте бота:**
    Создайте файл `.env` в той же директории. Как минимум, вы должны указать ваш `BOT_TOKEN`. Полный список переменных смотрите в разделе [Конфигурация](#-конфигурация)

4.  **Запустите бота:**
    ```bash
    docker-compose up -d
    ```

Бот запустится, создаст необходимые файлы и подключится к Telegram.

## 🛠️ Установка из исходного кода

<details>
<summary>Нажмите, чтобы развернуть инструкции по ручной установке</summary>

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Lowara1243/ocr-bot.git
    cd ocr-bot
    ```

2.  **Установите зависимости:**
    Мы рекомендуем использовать `uv`.
    ```bash
    # Создаст .venv и установит все зависимости из pyproject.toml
    uv pip install -e .
    ```

3.  **Настройте бота:**
    Скопируйте пример файла конфигурации и отредактируйте его своими настройками.
    ```bash
    cp .env.example .env
    nano .env
    ```

4.  **Запустите бота:**
    ```bash
    python -m src.ocr_bot.main
    ```
    </details>

## ⚙️ Конфигурация

Для настройки бота создайте файл `.env` в корневой директории проекта. Самый простой способ — скопировать файл-пример:

```bash
cp .env.example .env
```

Затем откройте `.env` в вашем редакторе и измените настройки.

| Переменная                | Описание                                                                     | Обязательно |
|:--------------------------|:-----------------------------------------------------------------------------|:-----------:|
| `BOT_TOKEN`               | Ваш токен Telegram бота от [@BotFather](https://t.me/BotFather).             |   **Да**    |
| `ADMIN_ID`                | Ваш Telegram User ID (у администратора нет лимитов).                         |     Нет     |
| `DEFAULT_OCR_ENGINE`      | OCR-движок по умолчанию (`tesseract` или `yandex`).                          |     Нет     |
| `ENABLED_OCR_ENGINES`     | Список включенных движков через запятую (например, `tesseract,yandex`).      |     Нет     |
| `YANDEX_CLOUD_API_KEY`    | API-ключ для Yandex Cloud Vision API.                                        |     Нет     |
| `YANDEX_CLOUD_FOLDER_ID`  | Идентификатор каталога для Yandex Cloud Vision API.                          |     Нет     |
| `RATE_LIMIT_DAILY`        | Дневной лимит запросов (целое число).                                        |     Нет     |
| `RATE_LIMIT_WEEKLY`       | Недельный лимит запросов (целое число).                                      |     Нет     |
| `RATE_LIMIT_MONTHLY`      | Месячный лимит запросов (целое число).                                       |     Нет     |
| `LOG_LEVEL`               | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.        |     Нет     |
| `LOG_FILE`                | Путь к файлу логов (оставьте пустым для вывода только в консоль).            |     Нет     |
| `DATABASE_PATH`           | Путь к файлу базы данных SQLite (например, `database/ocr_bot.db`).           |     Нет     |
| `TESSERACT_CMD_PATH`      | Полный путь к исполняемому файлу `tesseract`, если его нет в `PATH` системы. |     Нет     |
| `DEFAULT_OCR_LANGUAGE`    | Язык OCR по умолчанию (`eng`, `rus`, `eng+rus` и т.д.).                      |     Нет     |
| `SUPPORTED_OCR_LANGUAGES` | Список поддерживаемых языков через запятую (для Tesseract).                  |     Нет     |
| `OCR_LOG_PREVIEW_LENGTH`  | Количество символов для предпросмотра распознанного текста в логах.          |     Нет     |

## 🚦 Управление ботом

Основные команды для управления Docker-контейнером бота.

-   **Просмотр логов:**
    ```bash
    docker-compose logs -f
    ```

-   **Остановка бота:**
    ```bash
    docker-compose down
    ```

-   **Перезапуск бота:**
    ```bash
    docker-compose restart
    ```


## 🤝 Участие в проекте

Мы приветствуем любой вклад! Будь то отчеты об ошибках, предложения новых функций или pull-реквесты — все это ценится.

-   **Нашли ошибку?** Пожалуйста, используйте шаблон [Bug Report](https://github.com/Lowara1243/ocr-bot/issues/new?assignees=&labels=bug&template=bug_report.yml&title=%5BBUG%5D+) для создания issue.
-   **Есть идея для новой функции?** Откройте issue, чтобы обсудить ее.

## 📄 Лицензия

Этот проект лицензирован под лицензией MIT. Подробности смотрите в файле [LICENSE](LICENSE).