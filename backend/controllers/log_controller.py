from fastapi.responses import JSONResponse
from middleware.requestlog import file_lock, log_file, db_count_file

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
        "api_calls": api_calls,
        "db_accesses": db_accesses
    })