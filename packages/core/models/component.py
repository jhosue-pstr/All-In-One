from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from packages.core.models.base import BaseModel, TimestampMixin


class Component(BaseModel, TimestampMixin):
    __tablename__ = "components"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    html_template: Mapped[str] = mapped_column(Text, nullable=False)
    css_styles: Mapped[str | None] = mapped_column(Text, nullable=True)
    js_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    props_schema: Mapped[str] = mapped_column(Text, default="{}")
    category: Mapped[str] = mapped_column(String(50), default="basic")
    icon: Mapped[str] = mapped_column(String(50), default="box")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
