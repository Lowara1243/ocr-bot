[English](README.md) | [Русский](README.ru.md)

---

# Telegram OCR Bot

Телеграм-бот, который использует Tesseract или Yandex Vision для распознавания текста на изображениях.

## Оглавление
- [Возможности](#возможности)
- [Быстрый старт (Docker Compose)](#быстрый-старт-docker-compose)
- [Настройка и установка](#настройка-и-установка)
- [Установка из исходников](#установка-из-исходников)
- [Конфигурация](#конфигурация)
- [Управление ботом](#управление-ботом)

## Возможности
- Распознаёт текст на присланных фотографиях.
- **Несколько движков OCR:** локальный Tesseract и облачный Yandex Vision.
- **Постоянное хранение:** SQLite для данных пользователей и настроек.
- **Гибкая система лимитов:** настраиваемые дневные, недельные и месячные лимиты.
- **Готов к деплою:** оптимизирован для Docker Compose / Podman Compose.

## Быстрый старт (Docker Compose)
1. Создайте новую папку и поместите в неё `docker-compose.yml`.
2. Скопируйте пример файла окружения:
    ```bash
    cp .env.example .env
    ```
3. Отредактируйте `.env`, указав как минимум `BOT_TOKEN`.
4. Создайте `docker-compose.yml` со следующим содержимым, заменив `YOUR_USERNAME`, если вы выкладываете образ сами:
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
5. Запустите:
    ```bash
    docker-compose up -d
    ```
6. Бот запустится и подключится к Telegram по вашему токену.

## Установка из исходников
<details>
<summary>Нажмите, чтобы развернуть инструкцию</summary>

1. **Клонируйте репозиторий**
    ```bash
    git clone https://github.com/Lowara1243/ocr-bot.git
    cd ocr-bot
    ```
2. **Создайте виртуальное окружение и установите зависимости**
    - Рекомендуется с помощью `uv`:
        ```bash
        uv pip install -r requirements.txt
        ```
    - Стандартно через `pip`:
        ```bash
        python -m venv .venv
        source .venv/bin/activate     # Windows: .venv\Scripts\activate
        pip install -r requirements.txt
        ```
3. **Настройка окружения**
    ```bash
    cp .env.example .env
    ```
    Заполните как минимум `BOT_TOKEN`; подробности в [Конфигурация](#конфигурация).
4. **Запуск бота**
    ```bash
    python main.py
    ```
</details>

## Конфигурация
Скопируйте `.env.example` в `.env` и отредактируйте:

| Переменная                | Описание                                                              | Обязательно |
|:--------------------------|:----------------------------------------------------------------------|:-----------:|
| `BOT_TOKEN`               | Токен вашего бота от [@BotFather](https://t.me/BotFather).            |   **Да**    |
| `ADMIN_ID`                | Ваш Telegram User ID (админ без ограничений).                         |     Нет     |
| `DEFAULT_OCR_ENGINE`      | Движок OCR по умолчанию (`tesseract` или `yandex`).                   |     Нет     |
| `ENABLED_OCR_ENGINES`     | Список движков через запятую (`tesseract,yandex`).                    |     Нет     |
| `YANDEX_CLOUD_API_KEY`    | API-ключ Yandex Cloud для Yandex Vision API.                          |     Нет     |
| `YANDEX_CLOUD_FOLDER_ID`  | ID папки в Yandex Cloud для Yandex Vision API.                        |     Нет     |
| `RATE_LIMIT_DAILY`        | Суточный лимит запросов (целое число).                                |     Нет     |
| `RATE_LIMIT_WEEKLY`       | Недельный лимит запросов (целое число).                               |     Нет     |
| `RATE_LIMIT_MONTHLY`      | Месячный лимит запросов (целое число).                                |     Нет     |
| `LOG_LEVEL`               | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. |     Нет     |
| `LOG_FILE`                | Имя файла логов (оставьте пустым для вывода в консоль).               |     Нет     |
| `DATABASE_PATH`           | Путь до SQLite-файла (например `database/ocr_bot.db`).                |     Нет     |
| `TESSERACT_CMD_PATH`      | Полный путь к `tesseract`, если не в системном `PATH`.                |     Нет     |
| `DEFAULT_OCR_LANGUAGE`    | Язык OCR по умолчанию (`eng`, `rus`, `eng+rus` и т.п.).               |     Нет     |
| `SUPPORTED_OCR_LANGUAGES` | Поддерживаемые языки через запятую (для Tesseract).                   |     Нет     |
| `OCR_LOG_PREVIEW_LENGTH`  | Длина предпросмотра текста в логах (в символах).                      |     Нет     |

## Управление ботом
- **Просмотр логов:**  
  ```bash
  docker-compose logs -f
  ```

* **Остановка бота:**

  ```bash
  docker-compose down
  ```
* **Перезапуск бота:**

  ```bash
  docker-compose restart
  ```
