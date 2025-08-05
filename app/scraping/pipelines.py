from sqlalchemy import text

from ..db.session import async_session


async def save_item(data: dict) -> None:
    """Persist scraped item in the database using async_session."""
    query = text("INSERT INTO scraped_data (title) VALUES (:title)")
    async with async_session() as session:
        await session.execute(query, {"title": data["title"]})
        await session.commit()
