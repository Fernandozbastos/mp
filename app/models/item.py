from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class Item(Base):
    """Simple item model."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
