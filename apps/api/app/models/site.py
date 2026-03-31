from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel


class Site(BaseModel):
    __tablename__ = "sites"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="sites")
    pages: Mapped[list["Page"]] = relationship("Page", back_populates="site", cascade="all, delete-orphan")


from app.models.user import User
from app.models.page import Page
