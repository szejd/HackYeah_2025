"""Pytest configuration and fixtures for testing."""

import os
import pytest
from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI

# Set test database configuration before importing app
os.environ["DB_TYPE"] = "sqlite"
os.environ["DB_NAME"] = ":memory:"

from app.schemas.db_models import Base
from app.db_handler.db_connection import get_db


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine with proper SQLite configuration."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=False
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_app(test_db):
    """Create a test FastAPI app without lifespan events."""

    # Create a minimal lifespan that doesn't init the database
    @asynccontextmanager
    async def test_lifespan(app: FastAPI):
        yield

    # Import routers
    from app.routes import user, health_check, navigation

    # Create new app instance for testing
    app = FastAPI(
        title="Test API",
        description="Test API",
        version="1.0.0",
        lifespan=test_lifespan,
    )

    # Include the same routers
    app.include_router(health_check.router)
    app.include_router(user.router)
    app.include_router(navigation.router)

    # Override the database dependency
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield app

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(test_app):
    """Create a test client."""
    with TestClient(test_app, raise_server_exceptions=False) as test_client:
        yield test_client
