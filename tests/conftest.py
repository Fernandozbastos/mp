import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base


@pytest.fixture(scope="module")
def app_instance():
    """Provide the FastAPI application instance."""
    return app


@pytest.fixture(scope="module")
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSession()
    yield session
    session.close()
    engine.dispose()
