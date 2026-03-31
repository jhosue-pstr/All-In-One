from sqlalchemy import String, Text, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Page(BaseModel):
    __tablename__ = "pages"

    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    gjs_data: Mapped[str] = mapped_column(Text, nullable=True)
    gjs_html: Mapped[str] = mapped_column(Text, nullable=True)
    gjs_css: Mapped[str] = mapped_column(Text, nullable=True)
    is_home: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    meta_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    site: Mapped["Site"] = relationship("Site", back_populates="pages")


from app.models.site import Site
