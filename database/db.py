#Creates and connects the database connection.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from core.config import settings

database_url = settings.DATABASE_URL

engine=create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()