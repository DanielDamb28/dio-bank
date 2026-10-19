from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import db

class Role(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates='role')