"""FastAPI application for the Healthy Bite backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.modules.blog import router as blog_router
from app.modules.contact import router as contact_router
from app.modules.ai import router as ai_router

app = FastAPI(title="Healthy Bite Backend")

# CORS: разрешаем фронту ходить на бэкенд
# Фронт у тебя крутится на 127.0.0.1:8080 (python -m http.server 8080)
ALLOWED_ORIGINS = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


# API routers
app.include_router(blog_router.router, prefix="/api/v1/blog", tags=["blog"])
app.include_router(contact_router.router, prefix="/api/v1/contact", tags=["contact"])
app.include_router(ai_router.router, prefix="/api/v1/ai", tags=["ai"])

# Create database tables on startup (lightweight for this app)
Base.metadata.create_all(bind=engine)
