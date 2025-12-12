"""FastAPI routes for the Blog module."""

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session

from app.modules.common.deps import get_db
from . import service, schemas

router = APIRouter()


@router.get("/sections", response_model=schemas.BlogSectionsResponse)
def read_blog_sections(lang: str = Query("en", regex="^(en|ru|am)$"), db: Session = Depends(get_db)):
    return service.get_sections(db=db, lang=lang)


@router.get("/posts/{slug}", response_model=schemas.BlogPostFull)
def read_blog_post(
    slug: str = Path(..., min_length=1),
    lang: str = Query("en", regex="^(en|ru|am)$"),
    db: Session = Depends(get_db),
):
    return service.get_post_by_slug(db=db, slug=slug, lang=lang)
