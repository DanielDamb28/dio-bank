from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .base import db
from datetime import datetime
from sqlalchemy import ForeignKey

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]= mapped_column(nullable=False)
    body: Mapped[str]= mapped_column(nullable=False)
    created:Mapped[datetime] = mapped_column(server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self):
        return f"Post( id={self.id!r}, title={self.title!r}, authorId={self.author_id!r} )"