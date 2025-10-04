import logging
from typing import Generator

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from app.schemas.db_models import Base
from app.config import DB_NAME, DB_TYPE, DB_USER, DB_PASSWORD
from app.db_handler.db_util import ConnectionStringBuilder

logger = logging.getLogger(__name__)


def create_db_engine(echo: bool = False) -> Engine:
    """
    Create and configure the database engine.

    Args:
        echo: If True, SQLAlchemy will log all SQL statements

    Returns:
        Engine: Configured SQLAlchemy engine
    """
    db_conn = ConnectionStringBuilder.build(DB_TYPE, DB_NAME, DB_USER, DB_PASSWORD)
    try:
        engine = create_engine(
            db_conn,
            echo=echo,
            future=True,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before using them
            pool_recycle=3600,  # Recycle connections after 1 hour
        )
        logger.info(f"Database engine created successfully for: {DB_NAME}")
        return engine
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise


def init_db(engine: Engine) -> None:
    """
    Initialize the database by creating all tables.

    Args:
        engine: SQLAlchemy engine instance
    """
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise


# Create engine and session factory
engine = create_db_engine(echo=True)
init_db(engine)

# Create a session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
    expire_on_commit=False,  # Don't expire objects after commit
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    This generator function ensures proper session lifecycle:
    - Creates a new session for each request
    - Automatically closes the session after use
    - Handles exceptions gracefully

    Yields:
        Session: SQLAlchemy database session

    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
