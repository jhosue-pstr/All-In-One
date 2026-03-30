from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://cms_user:cms_pass@localhost:5432/cms_db"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
