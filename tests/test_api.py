import asyncio
from sqlalchemy import Column, Integer, String

from app.db.base import Base
from app.api.routes import read_root
from app.main import health_check


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


def test_read_root(app_instance) -> None:
    response = asyncio.run(read_root())
    assert response == {"message": "Welcome to mp API"}


def test_health_check(app_instance) -> None:
    response = asyncio.run(health_check())
    assert response == {"status": "ok"}


def test_crud_operations(db_session) -> None:
    item = Item(name="test")
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    assert item.id is not None

    fetched = db_session.get(Item, item.id)
    assert fetched.name == "test"

    fetched.name = "updated"
    db_session.commit()
    db_session.refresh(fetched)
    assert fetched.name == "updated"

    db_session.delete(fetched)
    db_session.commit()
    assert db_session.get(Item, item.id) is None
