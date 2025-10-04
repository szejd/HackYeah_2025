from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DB_NAME
from schemas.db_models import Base

engine = create_engine(DB_NAME, echo=True, future=True)

# Create all tables in the database (use your Base)
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
