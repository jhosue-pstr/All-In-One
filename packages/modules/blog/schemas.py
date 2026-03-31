from pydantic import BaseModel


class CategorySchema(BaseModel):
    name: str
    slug: str
    description: str | None = None


class PostSchema(BaseModel):
    title: str
    slug: str
    content: str = ""
    excerpt: str | None = None
    featured_image: str | None = None
    is_published: bool = False
