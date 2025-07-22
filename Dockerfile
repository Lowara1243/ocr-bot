FROM docker.io/library/python:3.10-slim AS builder

WORKDIR /app

COPY pyproject.toml .
COPY src/ocr_bot/ src/ocr_bot/

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache .


FROM docker.io/library/python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY src/ocr_bot/ src/ocr_bot/

CMD ["python", "-m", "src.ocr_bot.main"]