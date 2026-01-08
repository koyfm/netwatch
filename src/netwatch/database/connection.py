from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from netwatch.config import settings

engine = create_engine(settings.database.url)
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    """Get a database session with context management"""
    return SessionLocal()
