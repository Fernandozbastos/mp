from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from pydantic import BaseModel


from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import async_session
from ..models import Item
from .schemas.item import ItemCreate, ItemRead, ItemUpdate


from ..auth.jwt import create_access_token, get_token_subject
from ..auth.security import get_password_hash, verify_password

router = APIRouter()

fake_users_db: dict[str, str] = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class UserCreate(BaseModel):
    username: str
    password: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        username = get_token_subject(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return username


@router.post("/register", status_code=201)
async def register(user: UserCreate) -> dict[str, str]:
    """Register a new user."""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = hashed_password
    return {"username": user.username}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Authenticate a user and return an access token."""
    hashed_password = fake_users_db.get(form_data.username)
    if not hashed_password or not verify_password(form_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = create_access_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with async_session() as session:
        yield session


@router.get("/")
async def read_root(current_user: str = Depends(get_current_user)) -> dict[str, str]:
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
