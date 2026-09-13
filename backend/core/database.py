"""
Database Engine & Session Management
SIH26001 — Sikkim Historical Landslide Intelligence System (Phase 1)
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core.config import DATABASE_URL

# SQLAlchemy Base Class
Base = declarative_base()

# SQLAlchemy Engine
# Note: For Phase 1 scaffold, engine is created with pool_pre_ping=True
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Dependency for API routes to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
