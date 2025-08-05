from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import async_session
from ..models import Item
from .schemas.item import ItemCreate, ItemRead, ItemUpdate

router = APIRouter()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with async_session() as session:
        yield session


@router.get("/")
async def read_root() -> dict[str, str]:
    """Root API endpoint."""
    return {"message": "Welcome to mp API"}


@router.post("/items", response_model=ItemRead)
async def create_item(
    item: ItemCreate, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    """Create a new item."""
    db_item = Item(**item.dict())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.get("/items/{item_id}", response_model=ItemRead)
async def get_item(
    item_id: int, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    """Retrieve a single item by ID."""
    result = await session.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/items/{item_id}", response_model=ItemRead)
async def update_item(
    item_id: int, item: ItemUpdate, session: AsyncSession = Depends(get_session)
) -> ItemRead:
    """Update an existing item."""
    result = await session.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int, session: AsyncSession = Depends(get_session)
) -> dict[str, bool]:
    """Delete an item by ID."""
    result = await session.execute(select(Item).where(Item.id == item_id))
    db_item = result.scalar_one_or_none()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await session.delete(db_item)
    await session.commit()
    return {"ok": True}
