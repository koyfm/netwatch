import datetime

from sqlalchemy import DateTime, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("post_id", "comment_id"),)

    provider: Mapped[str] = mapped_column(primary_key=True)
    post_id: Mapped[str] = mapped_column(primary_key=True)
    comment_id: Mapped[str] = mapped_column(primary_key=True)
    url: Mapped[str]
    author: Mapped[str]
    title: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
