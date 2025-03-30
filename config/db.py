from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()


DB_URL= os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("DATABASE_URL is not set in the enviorment or .env file")


engine = create_engine(DB_URL)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

try:
    with engine.connect() as connection:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Failed to connect to the database:", e)