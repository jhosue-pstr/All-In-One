from sqlalchemy import String, Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from packages.core.models.base import BaseModel, TimestampMixin


class Category(BaseModel, TimestampMixin):
    __tablename__ = "blog_categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class Post(BaseModel, TimestampMixin):
    __tablename__ = "blog_posts"

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("blog_categories.id", ondelete="SET NULL"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    featured_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False)
