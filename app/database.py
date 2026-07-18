"""
Database configuration for Bhagalpur Stays
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:Raj%407744@localhost:3306/bhagalpur_stays"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=0,
    pool_recycle=3600,
    echo=False  # Set to True for SQL debugging
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency that creates a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Run once at startup."""
    Base.metadata.create_all(bind=engine)