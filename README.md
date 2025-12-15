# Healthy Bite

Healthy Bite is a small prototype with a static frontend and a FastAPI backend that serves a multilingual blog, contact forms, and an AI chat endpoint (OpenAI when configured, mock fallback otherwise).

## Tech stack
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic v2, Uvicorn
- Frontend: Vanilla HTML/CSS/JS (no build step)

## Quick start (dev)
1) Create venv & install backend deps  
   - Windows: `python -m venv .venv && .\.venv\Scripts\Activate.ps1`  
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`  
   - Install: `pip install -r backend/requirements.txt`
2) Copy env file: `cp backend/.env.example backend/.env` (or `copy backend\.env.example backend\.env` on Windows)
3) Run: `python run_dev.py`  
   - Backend: http://127.0.0.1:8810  
   - Frontend: http://127.0.0.1:8080  
   - Docs (if enabled): http://127.0.0.1:8810/docs

## Configuration (backend)
- `APP_ENV` (dev|prod, default dev): dev auto-creates DB tables on startup; prod skips unless `DB_AUTO_CREATE=true`.
- `DB_AUTO_CREATE` (default false): force table creation outside dev.
- `AI_PROVIDER` (mock|openai, default mock) + `OPENAI_API_KEY`/`OPENAI_MODEL`/`OPENAI_BASE_URL`: OpenAI used when configured; otherwise mock reply. Failures fall back to mock.
- `LOG_LEVEL` (default INFO): applied to FastAPI/uvicorn loggers.
- `ENABLE_DOCS` (true|false): toggle OpenAPI/docs routes.
- CORS: `CORS_ALLOW_ORIGINS` (comma list, default includes `http://127.0.0.1:8080`), `CORS_ALLOW_CREDENTIALS`, `CORS_ALLOW_METHODS`, `CORS_ALLOW_HEADERS`.
- `APP_PORT`, `DATABASE_URL` as usual (SQLite file by default).

## Smoke tests
- With backend running: `python backend/smoke_test.py`  
  Optional env: `BASE_URL` (default http://127.0.0.1:8810), `LANG` (en|ru|am).
  Exit code 0 = all checks pass.

## Notes
- AI chat prefers OpenAI when configured; any error falls back to the deterministic mock response.
- Docs are available only when `ENABLE_DOCS=true` (recommended off in prod).
- Database tables create at startup only in dev or when `DB_AUTO_CREATE=true`.




Healthy Bite

Healthy Bite — это аккуратно стабилизированный прототип веб-проекта с:

многоязычным контентным блогом,

формами обратной связи,

AI-чатом с безопасным fallback,

простым и воспроизводимым dev-окружением.

Проект ориентирован на читаемую архитектуру, предсказуемое поведение и отсутствие скрытой магии.
Подходит как база для дальнейшего развития (контент, UX, прод-деплой), так и как демонстрационный reference-проект.

Что реализовано
Backend

REST API на FastAPI

Многоязычный блог (EN / RU / AM) с fallback-логикой

Контактные формы (support / consult)

AI-чат:

mock-провайдер по умолчанию (детерминированный, для dev/demo)

OpenAI-провайдер при наличии ключа

любой сбой OpenAI → автоматический fallback на mock

SQLite по умолчанию, готовность к Postgres

Чётко контролируемое поведение dev / prod

Frontend

Статический фронт (HTML / CSS / Vanilla JS)

Без сборщиков, без Node.js

Запускается через http.server

Работает напрямую с backend API

Технологический стек

Backend

Python 3.10+

FastAPI

SQLAlchemy 2.x

Pydantic v2

Uvicorn

SQLite (через DATABASE_URL)

Frontend

Vanilla HTML / CSS / JavaScript

Без build-шага

Архитектура (кратко)
HealthyBiteSite/
│
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI app + middleware
│   │   ├── config.py      # Env-based settings (.env loader)
│   │   ├── db.py          # SQLAlchemy engine / Base
│   │   └── modules/
│   │       ├── blog/
│   │       ├── contact/
│   │       └── ai/
│   ├── requirements.txt
│   ├── .env.example
│   └── smoke_test.py
│
├── frontend/
│   ├── blog.html
│   ├── css/
│   ├── js/
│   └── lang/
│
├── run_dev.py             # one-command dev runner
└── README.md

Быстрый старт (dev)
1. Виртуальное окружение и зависимости
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate

pip install -r backend/requirements.txt

2. Конфигурация
# Windows
copy backend\.env.example backend\.env

# macOS / Linux
cp backend/.env.example backend/.env

3. Запуск
python run_dev.py


Доступно:

Backend API: http://127.0.0.1:8810

Frontend: http://127.0.0.1:8080

Swagger (если включён): http://127.0.0.1:8810/docs

Конфигурация backend (env)
Основные

APP_ENV — dev | prod (по умолчанию dev)

LOG_LEVEL — INFO, WARNING, ERROR

ENABLE_DOCS — включает/выключает /docs и /openapi.json

База данных

DATABASE_URL — по умолчанию sqlite:///healthybite.db

DB_AUTO_CREATE

dev: таблицы создаются автоматически

prod: не создаются, если явно не указано DB_AUTO_CREATE=true

AI

AI_PROVIDER — mock | openai

OPENAI_API_KEY

OPENAI_MODEL (по умолчанию gpt-4.1-mini)

OPENAI_BASE_URL (опционально)

Поведение:

OpenAI используется только если сконфигурирован

Любая ошибка → fallback на mock

Сервер никогда не падает из-за AI

CORS

CORS_ALLOW_ORIGINS — список через запятую
(по умолчанию включает http://127.0.0.1:8080)

CORS_ALLOW_CREDENTIALS

CORS_ALLOW_METHODS

CORS_ALLOW_HEADERS

Smoke-tests

Быстрая проверка всех ключевых сценариев API.

python backend/smoke_test.py


Опциональные переменные:

BASE_URL (по умолчанию http://127.0.0.1:8810)

LANG — en, ru, am (по умолчанию en)

Результат:

Exit code 0 → всё работает

Exit code 1 → есть проблема (печатается причина)

Принципы проекта

❌ нет скрытых сайд-эффектов при импорте

❌ нет “магии” в проде

✅ всё поведение управляется env-переменными

✅ dev-удобство не ломает prod-безопасность

✅ код читается и предсказуем

Статус

Проект находится в стабильной, зафиксированной точке:

окружение воспроизводимо,

прод-риски закрыты,

smoke-проверки есть,

можно либо деплоить, либо развивать продуктовую часть.