from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import threading
import os
import datetime

log_file = "logs.txt"
db_count_file = "db_count.txt"
file_lock = threading.Lock()

async def log_requests(request: Request, call_next):
    #the request method_
    method = request.method
    #The route used in request
    path = request.url.path
    #Time the request was made:
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    #entry string for the logs
    log_entry = f"{method} {path} {time}\n"

    with file_lock:
        with open(log_file, "a") as f:
            f.write(log_entry)

    response = await call_next(request)
    return response


def increment_db_access():
    with file_lock:
        if not os.path.exists(db_count_file):
            with open(db_count_file, "w") as f:
                f.write("0")
        with open(db_count_file, "r+") as f:
            count = int(f.read())
            f.seek(0)
            f.write(str(count + 1))
            f.truncate()