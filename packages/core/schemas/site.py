from datetime import datetime
from pydantic import BaseModel, Field


class SiteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")


class SiteCreate(SiteBase):
    pass


class SiteResponse(SiteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
