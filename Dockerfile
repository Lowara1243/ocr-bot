FROM docker.io/library/python:3.10-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r requirements.txt


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
COPY . .

CMD ["python", "main.py"]