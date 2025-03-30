from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os


DB_URL= os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/mydatabase")

engine = create_engine(DB_URL)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()