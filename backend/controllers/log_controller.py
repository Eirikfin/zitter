from fastapi.responses import JSONResponse
from models import Db_Accessed, Log
from config.db import SessionLocal

"""
def getLogs():
    with file_lock:
        with open(log_file, "r") as f:
            api_calls = [line.strip().split(" ") for line in f.readlines()]
        try:
            with open(db_count_file, "r") as f:
                db_accesses = int(f.read())
        except FileNotFoundError:
            db_accesses = 0
    return JSONResponse(content={
        "db_accesses": db_accesses,
        "api_calls": api_calls
       
    })
"""


def getLogs():
    db = SessionLocal
    try:
        db_amount = db.query(Db_accessed).first()
        logs = db.query(Log).all()

        result = {
            "times_db_was_accessed": db_amount.amount if db_amount else 0,
            "logs": [
                {
                    "method": log.method,
                    "path": log.path,
                    "time": log.time.strftime("%Y-%m-%d %H:%M:%S")
                } for log in logs
            ]
        }

        return result
    finally:
        db.remove()
