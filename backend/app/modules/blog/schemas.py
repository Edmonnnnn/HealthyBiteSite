"""Data schemas for the Blog module."""

from typing import List, Optional, Union, Literal

from pydantic import BaseModel


class BlogFilter(BaseModel):
    id: str
    label: str
    class Config:
        orm_mode = True


class BlogHero(BaseModel):
    eyebrow: str
    title: str
    lead: str
    searchPlaceholder: str
    filters: List[BlogFilter]
    class Config:
        orm_mode = True


class BlogPostShort(BaseModel):
    id: int
    slug: str
    eyebrow: Optional[str] = None
    title: str
    summary: str
    section: str
    readingMinutes: int
    tags: List[str]
    imageUrl: Optional[str] = None
    publishedAt: str
    class Config:
        orm_mode = True


class BlogSection(BaseModel):
    title: str
    items: List[BlogPostShort]
    class Config:
        orm_mode = True


class BlogSections(BaseModel):
    weekly: BlogSection
    featured: BlogSection
    trending: BlogSection
    success: BlogSection
    tips: BlogSection
    mindset: BlogSection
    routine: BlogSection
    all: BlogSection
    class Config:
        orm_mode = True


class BlogSectionsResponse(BaseModel):
    lang: str
    hero: BlogHero
    sections: BlogSections
    class Config:
        orm_mode = True


class ContentBlockParagraph(BaseModel):
    type: Literal["paragraph"]
    text: str
    class Config:
        orm_mode = True


class ContentBlockList(BaseModel):
    type: Literal["list"]
    items: List[str]
    class Config:
        orm_mode = True


class ContentBlockQuote(BaseModel):
    type: Literal["quote"]
    text: str
    author: Optional[str] = None
    class Config:
        orm_mode = True


class ContentBlockTip(BaseModel):
    type: Literal["tip"]
    title: str
    text: str
    class Config:
        orm_mode = True


ContentBlock = Union[ContentBlockParagraph, ContentBlockList, ContentBlockQuote, ContentBlockTip]


class BlogPostFull(BaseModel):
    lang: str
    id: int
    slug: str
    eyebrow: Optional[str] = None
    title: str
    summary: str
    readingMinutes: int
    tags: List[str]
    imageUrl: Optional[str] = None
    publishedAt: str
    contentBlocks: List[ContentBlock]
    class Config:
        orm_mode = True
