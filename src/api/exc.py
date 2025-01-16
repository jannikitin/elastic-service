from fastapi import HTTPException
from starlette import status


forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
)
