FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app

# 한글 폰트 설치 (나무위키 렌더링용)
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data

ENV DB_PATH=/data/rankings.db

# 단일 워커 + 멀티 스레드 (Playwright 인스턴스 공유)
CMD gunicorn app:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 4 \
    --timeout 120 \
    --keep-alive 5
