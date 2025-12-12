"""SQLAlchemy models for the Blog module."""

from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.sql import func

from app.db import Base


class BlogPost(Base):
    __tablename__ = "blog_posts"
    __table_args__ = (UniqueConstraint("slug", "lang", name="uq_blog_posts_slug_lang"),)

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    section = Column(String, nullable=False)
    hero_image = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    lang = Column(String, default="en", nullable=False)
    content_blocks = Column(SQLiteJSON, nullable=True)
    eyebrow = Column(String, nullable=True)
    reading_minutes = Column(Integer, nullable=True)
    tags = Column(SQLiteJSON, nullable=True)
    published_at = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
