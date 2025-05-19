from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import threading
import os
import datetime
from models import Log, Db_Accessed
from sqlalchemy import desc
from sqlalchemy.orm import Session
from fastapi import Request
from config.db import SessionLocal 
#log_file = "logs.txt"
#db_count_file = "db_count.txt"
#file_lock = threading.Lock()
async def log_requests(request: Request, call_next):
    db = SessionLocal  # ← No parentheses here

    try:
        now = datetime.datetime.now()
        log_entry = Log(
            method=request.method,
            path=request.url.path,
            time=now.strftime("%Y-%m-%d %H:%M:%S")
        )
        db.add(log_entry)
        db.commit()
    finally:
        db.remove()  # ← Important: use .remove() for scoped_session cleanup

    response = await call_next(request)
    return response


def increment_db_access():
    db = SessionLocal

    try:
        amount = db.query(Db_accessed).first()

        if amount is None:
            # If no entry exists, create one
            amount = Db_accessed(amount=1)
            db.add(amount)
        else:
            amount.amount += 1

        db.commit()
        db.refresh(amount)

    finally:
        db.remove()  # clean up session





