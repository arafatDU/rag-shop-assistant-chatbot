from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# Create the SQLAlchemy engine with proper connection pooling and SSL settings
engine = create_engine(
    settings.database_url,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # This will validate connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args={
        "sslmode": "require",
        "options": "-c timezone=utc"
    }
)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

def create_tables():
    """Create all tables in the PostgreSQL database."""
    # Import models here to ensure they are registered with Base
    from . import models
    Base.metadata.create_all(bind=engine)
    print("📊 PostgreSQL tables created successfully!")

def get_db():
    """Dependency to get database session with proper error handling"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()