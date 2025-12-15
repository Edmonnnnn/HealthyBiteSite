"""Database-backed service layer for the Blog module."""

import json
from datetime import datetime
from typing import Dict, List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas

_HERO = schemas.BlogHero(
    eyebrow="Healthy Bite",
    title="Discover practical nutrition tips and inspiring success stories",
    lead="Fresh weekly insights on balanced meals, mindful habits, and real transformations.",
    searchPlaceholder="Search articles, topics, or tags",
    filters=[
        schemas.BlogFilter(id="all", label="All"),
        schemas.BlogFilter(id="nutrition", label="Nutrition"),
        schemas.BlogFilter(id="wellness", label="Wellness"),
        schemas.BlogFilter(id="habits", label="Habits"),
    ],
)

_SECTION_TITLES: Dict[str, str] = {
    "weekly": "This Week's Picks",
    "featured": "Featured",
    "trending": "Trending Now",
    "success": "Success Stories",
    "tips": "Quick Tips",
    "mindset": "Mindset",
    "routine": "Routine",
    "all": "All Articles",
}


def _parse_content_blocks(raw) -> List:
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return []
    return []


def _parse_tags(raw) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        return [t for t in raw.split(",") if t]
    return []


def _to_published_str(post: models.BlogPost) -> str:
    if post.published_at:
        return str(post.published_at)
    if post.created_at:
        return post.created_at.date().isoformat()
    return datetime.utcnow().date().isoformat()


def _to_short(post: models.BlogPost) -> schemas.BlogPostShort:
    tags = _parse_tags(getattr(post, "tags", None))
    return schemas.BlogPostShort(
        id=post.id,
        slug=post.slug,
        section=post.section,
        eyebrow=post.eyebrow,
        title=post.title,
        summary=post.summary or post.subtitle or "",
        readingMinutes=post.reading_minutes or 5,
        tags=tags,
        imageUrl=post.hero_image,
        publishedAt=_to_published_str(post),
    )


def _to_full(post: models.BlogPost, lang: str) -> schemas.BlogPostFull:
    content_blocks = _parse_content_blocks(getattr(post, "content_blocks", None))
    tags = _parse_tags(getattr(post, "tags", None))
    published_at = getattr(post, "published_at", None)
    if published_at:
        published_value = (
            published_at.isoformat() if hasattr(published_at, "isoformat") else str(published_at)
        )
    else:
        published_value = _to_published_str(post)
    return schemas.BlogPostFull(
        lang=lang,
        id=post.id,
        slug=post.slug,
        eyebrow=post.eyebrow,
        title=post.title,
        summary=post.summary or post.subtitle or "",
        readingMinutes=post.reading_minutes or 5,
        tags=tags,
        imageUrl=post.hero_image,
        publishedAt=published_value,
        contentBlocks=content_blocks,
    )


def _get_posts_by_lang(db: Session, lang: str) -> List[models.BlogPost]:
    return (
        db.query(models.BlogPost)
        .filter(models.BlogPost.lang == lang)
        .order_by(models.BlogPost.created_at.desc())
        .all()
    )


def get_sections(db: Session, lang: str = "en") -> schemas.BlogSectionsResponse:
    en_posts = _get_posts_by_lang(db, "en")

    if lang == "en":
        selected_posts = en_posts
    else:
        requested_posts = _get_posts_by_lang(db, lang)
        if not en_posts:
            selected_posts = requested_posts
        else:
            en_by_slug = {post.slug: post for post in en_posts}
            requested_by_slug = {post.slug: post for post in requested_posts}
            selected_posts = [requested_by_slug.get(slug, en_by_slug[slug]) for slug in en_by_slug]

    print("[HB db] BlogPost rows (selected):", len(selected_posts))

    grouped: Dict[str, List[schemas.BlogPostShort]] = {key: [] for key in _SECTION_TITLES}
    for post in selected_posts:
        short = _to_short(post)
        section_key = post.section if post.section in grouped else "all"
        grouped[section_key].append(short)
        if section_key != "all":
            grouped["all"].append(short)

    sections = schemas.BlogSections(
        weekly=schemas.BlogSection(title=_SECTION_TITLES["weekly"], items=grouped.get("weekly", [])),
        featured=schemas.BlogSection(title=_SECTION_TITLES["featured"], items=grouped.get("featured", [])),
        trending=schemas.BlogSection(title=_SECTION_TITLES["trending"], items=grouped.get("trending", [])),
        success=schemas.BlogSection(title=_SECTION_TITLES["success"], items=grouped.get("success", [])),
        tips=schemas.BlogSection(title=_SECTION_TITLES["tips"], items=grouped.get("tips", [])),
        mindset=schemas.BlogSection(title=_SECTION_TITLES["mindset"], items=grouped.get("mindset", [])),
        routine=schemas.BlogSection(title=_SECTION_TITLES["routine"], items=grouped.get("routine", [])),
        all=schemas.BlogSection(title=_SECTION_TITLES["all"], items=grouped.get("all", [])),
    )

    return schemas.BlogSectionsResponse(lang=lang, hero=_HERO, sections=sections)


def get_post_by_slug(db: Session, slug: str, lang: str = "en") -> schemas.BlogPostFull:
    post = (
        db.query(models.BlogPost)
        .filter(models.BlogPost.slug == slug, models.BlogPost.lang == lang)
        .first()
    )
    if not post and lang != "en":
        post = (
            db.query(models.BlogPost)
            .filter(models.BlogPost.slug == slug, models.BlogPost.lang == "en")
            .first()
        )

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Reuse the converter to normalize JSON/text fields into the response schema
    return _to_full(post, lang=getattr(post, "lang", lang))
