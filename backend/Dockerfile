# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --default-timeout=120 --retries 5 -r requirements.txt

COPY app ./app
COPY modelo_lexboe.joblib modelo_lexboe_info.json ./

ENV MODEL_PATH=/app/modelo_lexboe.joblib \
    INFO_PATH=/app/modelo_lexboe_info.json \
    PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
