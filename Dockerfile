# syntax=docker/dockerfile:1

# ---------- Stage 1: build del frontend ----------
FROM node:22-alpine AS frontend
WORKDIR /build/frontend

RUN corepack enable

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY frontend/ ./
RUN pnpm build

# ---------- Stage 2: backend + modelo + frontend compilado ----------
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencias del backend (versiones fijadas)
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --default-timeout=120 --retries 5 -r backend/requirements.txt

# Código del backend
COPY backend/app ./backend/app

# Modelo entrenado e información
COPY modelo_lexboe.joblib modelo_lexboe_info.json ./

# Frontend compilado
COPY --from=frontend /build/frontend/dist ./frontend/dist

WORKDIR /app/backend

ENV MODEL_PATH=/app/modelo_lexboe.joblib \
    INFO_PATH=/app/modelo_lexboe_info.json \
    FRONTEND_DIST=/app/frontend/dist \
    CORS_ORIGINS=http://localhost:8000 \
    PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
