import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from models.base import Base


# Load .env
load_dotenv()
print("DATABASE_URL from .env:", os.getenv("DATABASE_URL"))


# Get database URL
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

# Create engine
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})  # for SQLite

# Create session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for models
Base = declarative_base()

# Test DB connection
try:
    with engine.connect() as connection:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Failed to connect to the database:", e)
