import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import time
import logging
import sys
from pythonjsonlogger import jsonlogger
from models.base import Base  # keep your existing import

# Load .env
load_dotenv()
print("DATABASE_URL from .env (raw):", repr(os.getenv("DATABASE_URL")))

# Get database URL
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL is not set in the environment or .env file")

connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Setup DB logger
logger = logging.getLogger("fastapi.db")
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

def setup_sqlalchemy_logging(engine):
    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        start_time = conn.info['query_start_time'].pop(-1)
        duration_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            "db_query",
            extra={
                "type": "db_call",
                "statement": statement,
                "parameters": parameters,
                "duration_ms": duration_ms,
            }
        )

# Create engine and setup logging
engine = create_engine(DB_URL, connect_args=connect_args)
setup_sqlalchemy_logging(engine)

# Create session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Base class for models (keep your existing Base)
Base = declarative_base()

# Test DB connection
try:
    with engine.connect() as connection:
        print("✅ Successfully connected to the database!")
except Exception as e:
    print("❌ Failed to connect to the database:", e)
