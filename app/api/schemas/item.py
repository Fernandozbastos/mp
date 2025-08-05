from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str | None = None


class ItemCreate(ItemBase):
    """Schema for creating an item."""


class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ItemRead(ItemBase):
    id: int

    class Config:
        orm_mode = True
