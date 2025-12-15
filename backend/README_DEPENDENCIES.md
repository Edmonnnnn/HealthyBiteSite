# Backend Dependencies

Summary:
- Pinned the FastAPI stack to Python 3.10-compatible versions that work with Pydantic v2.
- Added missing direct imports (`pydantic`, `requests`) and pinned `openai` for the AI provider flow.
- Swapped `uvicorn[standard]` for `uvicorn` to keep the runtime minimal while retaining reload support.

Used / Unused / Uncertain:

| Package    | Status              | Notes                                                                                                                                       |
|------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| fastapi    | Used                | Core API framework (`app/main.py`, routers).                                                                                                |
| pydantic   | Used                | All response/request schemas in `app/modules/*/schemas.py`.                                                                                |
| SQLAlchemy | Used                | ORM for models and sessions (`app/db.py`, models/services).                                                                                |
| uvicorn    | Used                | Server entrypoint (`python -m uvicorn app.main:app` in `run_dev.py`).                                                                      |
| openai     | Used (conditional)  | Called when `AI_PROVIDER=openai` and `OPENAI_API_KEY` is set; otherwise the service falls back to the built-in mock reply.                 |
| requests   | Used                | HTTP checks in `run_full_test.py` and `run_super_test.py`.                                                                                 |

How to verify:
1) Create and activate a virtual env  
   - Windows (PowerShell): `python -m venv .venv; .\\.venv\\Scripts\\Activate.ps1`  
   - Linux/macOS (bash): `python3 -m venv .venv; source .venv/bin/activate`
2) Install deps: `pip install -r backend/requirements.txt`
3) Start the backend (from repo root): `python run_dev.py`  
   - or from `backend/`: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8810 --reload`
4) Smoke-test endpoints (replace `curl` with `Invoke-WebRequest` on Windows if preferred):  
   - Health: `curl http://127.0.0.1:8810/health`  
   - Blog sections: `curl http://127.0.0.1:8810/api/v1/blog/sections?lang=en`  
   - Contact support: `curl -X POST http://127.0.0.1:8810/api/v1/contact/support -H \"Content-Type: application/json\" -d '{\"name\":\"Test\",\"email\":\"test@example.com\",\"topic\":\"Check\",\"message\":\"Hello\",\"lang\":\"en\"}'`  
   - AI chat (mock by default): `curl -X POST http://127.0.0.1:8810/api/v1/ai/chat -H \"Content-Type: application/json\" -d '{\"lang\":\"en\",\"messages\":[{\"role\":\"user\",\"content\":\"Hello\"}]}'`
5) Optional OpenAI check: set `AI_PROVIDER=openai` and `OPENAI_API_KEY` (plus `OPENAI_MODEL`, `OPENAI_BASE_URL` if needed) before start; the service will attempt OpenAI first and fall back to mock on error.
