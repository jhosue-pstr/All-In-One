from datetime import datetime
from pydantic import BaseModel, Field


class ComponentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    html_template: str
    css_styles: str | None = None
    js_code: str | None = None
    props_schema: str = "{}"
    category: str = "basic"
    icon: str = "box"


class ComponentCreate(ComponentBase):
    pass


class ComponentResponse(ComponentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
