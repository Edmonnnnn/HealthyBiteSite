"""FastAPI application for the Healthy Bite backend."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.modules.blog import router as blog_router
from app.modules.contact import router as contact_router
from app.modules.ai import router as ai_router


def _configure_logging() -> None:
    level_name = (settings.LOG_LEVEL or "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(level=level)
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi"):
        logging.getLogger(name).setLevel(level)


_configure_logging()

docs_enabled = bool(settings.ENABLE_DOCS)
app = FastAPI(
    title="Healthy Bite Backend",
    docs_url="/docs" if docs_enabled else None,
    redoc_url="/redoc" if docs_enabled else None,
    openapi_url="/openapi.json" if docs_enabled else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS or ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=settings.CORS_ALLOW_HEADERS or ["*"],
)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


# API routers
app.include_router(blog_router.router, prefix="/api/v1/blog", tags=["blog"])
app.include_router(contact_router.router, prefix="/api/v1/contact", tags=["contact"])
app.include_router(ai_router.router, prefix="/api/v1/ai", tags=["ai"])

@app.on_event("startup")
def on_startup() -> None:
    should_create = settings.APP_ENV == "dev" or settings.DB_AUTO_CREATE
    if should_create:
        logging.getLogger(__name__).info(
            "DB auto-create enabled (APP_ENV=%s, DB_AUTO_CREATE=%s)", settings.APP_ENV, settings.DB_AUTO_CREATE
        )
        Base.metadata.create_all(bind=engine)
    else:
        logging.getLogger(__name__).info("DB auto-create skipped (APP_ENV=%s)", settings.APP_ENV)
