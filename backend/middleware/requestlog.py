from fastapi import Request
import time
import logging
import sys
from pythonjsonlogger import jsonlogger

# Define your own logger
logger = logging.getLogger("fastapi.request")
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    log_data = {
        "type": "request",
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": process_time,
        "client_ip": client_ip,
        "user_agent": user_agent,
    }

    # Log with structured message
    logger.info("request", extra=log_data)

    return response
