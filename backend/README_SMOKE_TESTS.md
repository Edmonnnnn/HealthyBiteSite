# Backend Smoke Tests

Quick, no-frills smoke checks for the running backend (FastAPI) that cover the main user flows.

## Prerequisites
- Backend is running (default: `http://127.0.0.1:8810`). Start via `python run_dev.py` or your usual command.
- Python with `requests` installed (already listed in backend requirements).

## How to run
```bash
python backend/smoke_test.py
```

Optional environment variables:
- `BASE_URL` (default: `http://127.0.0.1:8810`)
- `LANG` (default: `en`)

## What it does
The script runs in sequence:
1. `GET /health` — expects 200 and `{"status": "ok"}`.
2. `GET /api/v1/blog/sections?lang=<LANG>` — expects 200, presence of `lang/hero/sections`, and at least one section entry. Extracts a post slug when available.
3. `GET /api/v1/blog/posts/{slug}?lang=<LANG>` — validates post detail minimally (status 200, has `slug` and a title-like field).
4. `POST /api/v1/contact/support` — sends a small payload; expects 200 and success indicator.
5. `POST /api/v1/contact/consult` — similar minimal payload and validation.
6. `POST /api/v1/ai/chat` — sends a short chat message; expects 200 and a `reply` string.

Each step prints `[OK]` or `[FAIL]` with a short snippet on errors. Exit code is `0` only if all checks pass.

## Expected output
The script prints a checklist of each endpoint tested and ends with `Overall: PASS` (or `FAIL`). Any failures include HTTP status and a short response snippet (max ~300 chars) to help with quick triage.
