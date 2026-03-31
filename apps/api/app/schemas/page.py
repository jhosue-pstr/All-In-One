from datetime import datetime
from pydantic import BaseModel, Field


class PageBase(BaseModel):
    site_id: int
    title: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    content: str = ""
    is_home: bool = False
    is_published: bool = False
    meta_title: str | None = None
    meta_description: str | None = None


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None
    gjs_data: str | None = None
    gjs_html: str | None = None
    gjs_css: str | None = None
    is_home: bool | None = None
    is_published: bool | None = None
    meta_title: str | None = None
    meta_description: str | None = None


class PageResponse(PageBase):
    id: int
    gjs_data: str | None = None
    gjs_html: str | None = None
    gjs_css: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PageListResponse(BaseModel):
    id: int
    title: str
    slug: str
    is_home: bool
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True
