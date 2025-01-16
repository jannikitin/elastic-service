import logging
import time
import uuid

import uvicorn
from api.endpoints.admin_endpoints import admin_router
from api.endpoints.login_endpoints import login_router
from api.endpoints.user_endpoints import user_router
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from logging_config import FILE_LOGGER

file_logger = logging.getLogger(FILE_LOGGER)

app = FastAPI(title="Elastic")

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(login_router, prefix="/login", tags=["auth"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


@app.get("/")
async def root():
    10 / 0
    return {"message": "OK!"}


@app.middleware("http")
async def middleware(request: Request, call_next):
    request_id = uuid.uuid4()
    start_time = time.perf_counter()
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        file_logger.error(
            f"Exception for {request.method} [{request_id}] request\n"
            f"Error type: {error_type}, Message: {error_message}"
        )

        raise HTTPException(status_code=500, detail="Unexpected server error")
    finally:
        process_time = time.perf_counter() - start_time
        file_logger.info(f"{request.method} [{request_id}]: {process_time} seconds")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
