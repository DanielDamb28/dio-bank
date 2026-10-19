from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy as sa
from .base import db
from sqlalchemy import ForeignKey

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(default=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"),nullable=True)
    role: Mapped["Role"] = relationship(back_populates='user')
        

    def __repr__(self):
        return f"User( id={self.id!r}, username={self.username!r} )"